from urllib.parse import urlparse, urlunparse, urljoin
from pathlib import Path


def extract_base_url(url: str):
    parsed = urlparse(url)
    return urlunparse([parsed.scheme, parsed.netloc, "", "", "", ""])


def join_url_path(base: str, path: str):
    return urljoin(base, path)


def create_dir_if_not_exists(dir_path: str):
    Path(dir_path).mkdir(parents=True, exist_ok=True)
