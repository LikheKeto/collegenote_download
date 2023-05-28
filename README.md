# Collegenote Downloader

A script for downloading CSIT notes, past question papers and books from collegenote website.

## Usage

Install dependencies:
`pip install -r requirements.txt`

Run script:
`python3 cndownload`

```
usage: cndownload [-h] [-o OUTPUT] [-e [{books,pastpapers,notes} ...]] {1,2,3,4,5,6,7,8} [{1,2,3,4,5,6,7,8} ...]

downloads notes, past questions and books from collegenote and saves them in an organized manner

positional arguments:
  {1,2,3,4,5,6,7,8}     semesters to download files for

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        output dir to save files
  -e [{books,pastpapers,notes} ...], --exclude [{books,pastpapers,notes} ...]
                        files to exclude from downloading
```

> Only tested for 4th semeseter and may not work for other semesters
