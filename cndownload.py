import os
import yaml
import argparse
import requests
from bs4 import BeautifulSoup
from loguru import logger
from helpers import extract_base_url, join_url_path, create_dir_if_not_exists
import gdown

parser = argparse.ArgumentParser(
    prog='cndownload',
    description='downloads notes, past questions and books from collegenote and saves them in an organized manner',
    epilog='likheketo ko kaam'
)

parser.add_argument('-o', '--output', default='study_files',
                    help='output dir to save files')
parser.add_argument('semesters', nargs='+', type=int,
                    choices=[1, 2, 3, 4, 5, 6, 7, 8])
parser.add_argument('-e', '--exclude',
                    choices=['books', 'pastpapers', 'notes'], action='store', nargs="*")

args = parser.parse_args()
output_dir = args.output
semesters = args.semesters
exclusion_list = args.exclude
configs = {}

with open('configs.yaml', 'r') as cf:
    try:
        configs = yaml.safe_load(cf)
    except yaml.YAMLError as exc:
        logger.exception(exc)


def download_notes(link: str, output_dir: str):
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'html5lib')

    # with open('notes.html', 'w') as f:
    # f.write(str(r.content))
    # with open('notes.html', 'r') as f:
    #     content = f.read()
    # soup = BeautifulSoup(content, 'html5lib')

    download_links = []

    for dl in soup.findAll('a', href=True, attrs={'target': 'blank'}):
        download_links.append({
            'title': dl.find_previous_sibling('h4').text.replace('\\n', '').strip()+".pdf",
            'link': dl['href']
        })

    create_dir_if_not_exists(output_dir)
    for dl in download_links:
        output = os.path.join(output_dir, dl['title'])
        if os.path.exists(output):
            logger.info(f'note {output} already exists, skipping!')
            continue
        gdown.download(dl['link'], output=output)


def download_pastpapers(link: str, output_dir: str):
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'html5lib')

    # with open('pastpapers.html', 'w') as f:
    #    f.write(str(r.content))
    # with open('pastpapers.html', 'r') as f:
    #     content = f.read()
    # soup = BeautifulSoup(content, 'html5lib')

    download_links = []
    base_url = extract_base_url(link)

    for cards in soup.findAll('div', attrs={'class': 'card-body'}):
        download_links.append({
            'title': cards.find('h4').text.replace('\\n', '').strip()+".pdf",
            'link':  os.path.join(base_url+cards.find_all('a')[1]['href'])
        })
    create_dir_if_not_exists(output_dir)
    for dl in download_links:
        output = os.path.join(output_dir, dl['title'])
        if os.path.exists(output):
            logger.info(f'pastpaper {output} already exists, skipping!')
            continue
        logger.info(f'downloading past paper - {output}')
        r = requests.get(dl['link'])
        open(output, 'wb').write(r.content)


def download_books(link: str, output_dir: str):
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'html5lib')

    # with open('books.html', 'w') as f:
    #     f.write(str(r.content))
    # with open('books.html', 'r') as f:
    #     content = f.read()
    # soup = BeautifulSoup(content, 'html5lib')

    download_link = soup.find('a', href=True, string='here')['href']
    if os.path.exists(output_dir):
        logger.info(f'book dir - {output_dir} already exists, skipping!')
        return
    gdown.download_folder(download_link, output=output_dir)
    print(download_link)


def download_for_subject(link: list, output_dir: str):
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'html5lib')
    base_url = extract_base_url(r.url)

    # with open('test.html', 'w') as f:
    #     f.write(str(r.content))
    # with open('test.html', 'r') as f:
    #     content = f.read()
    # soup = BeautifulSoup(content, 'html5lib')
    # base_url = 'https://www.collegenote.net'

    if 'notes' not in exclusion_list:
        notes_path = soup.find('a', href=True, string='Notes')['href']
        download_notes(join_url_path(base_url, notes_path),
                       os.path.join(output_dir, 'notes'))

    if 'pastpapers' not in exclusion_list:
        pastpapers_path = soup.find(
            'a', href=True, string='Questions & solutions')['href']
        download_pastpapers(join_url_path(base_url, pastpapers_path),
                            os.path.join(output_dir, 'pastpapers'))
    if 'books' not in exclusion_list:
        books_path = soup.find(
            'a', href=True, string='Text & reference books')['href']
        download_books(join_url_path(base_url, books_path),
                       os.path.join(output_dir, 'books'))


def download_semester_files(subjects: list, output_dir: str):
    for subject, link in subjects.items():
        logger.info(f'downloading files for {subject}')
        download_for_subject(
            link, output_dir=os.path.join(output_dir, subject))
        logger.info(f'finished downloading all files of {subject}')


for semester in semesters:
    logger.info(f'downloading files for semester-{semester}')
    download_semester_files(configs[semester], os.path.join(
        output_dir, f'semester-{semester}'))
    logger.info(f'finished downloading all files for semester-{semester}')

logger.info('Completed downloading all files!')
