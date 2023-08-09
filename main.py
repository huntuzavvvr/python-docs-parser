import re
from urllib.parse import urljoin
import requests_cache
from tqdm import tqdm
from bs4 import BeautifulSoup
import logging
from constants import BASE_DIR, MAIN_DOC_URL
from configs import configure_parser, configure_logging
from utils import get_response, find_parse
from outputs import *


def whats_new(session):
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    response = get_response(session, whats_new_url)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, 'lxml')
    sect = find_parse(soup, "section", attrs={"id": "what-s-new-in-python"})
    l1 = find_parse(sect, "div").find_all(class_="toctree-l1")
    results = [("Link to docs", "Name", "Author/Editor")]
    for i in tqdm(l1):
        a = find_parse(i, "a")
        href = a.get("href")
        full_link = urljoin(whats_new_url, href)
        session = requests_cache.CachedSession()
        response = session.get(full_link)
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, 'lxml')
        sec = find_parse(soup, "section")
        title = find_parse(sec, "h1").text
        descr = find_parse(sec, "dl").text
        descr = descr.replace("\n", ' ')
        results.append((full_link, title[:-1], descr))
    return results


def latest_versions(session):
    response = get_response(session, MAIN_DOC_URL)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "lxml")
    links = find_parse(find_parse(soup, "div", attrs={"class": "sphinxsidebarwrapper"}), "ul")
    for i in links:
        if "All version" in i.text:
            a_tags = links.find_all("a")
            break
    else:
        raise Exception("Nothing")
    results = [("Link to docs", "Version", "Status")]
    pattern = r'Python (\d.\d+) \((.*)\)'
    for a_tag in a_tags:
        link = a_tag['href']
        text_match = re.search(pattern, a_tag.text)
        if text_match is not None:
            version, status = text_match.groups()
        else:
            try:
                version, status = float(a_tag.text), ''
            except Exception as error:
                version, status = a_tag.text, ''
        results.append(
            (link, version, status)
        )
    return results


def download(session):
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    necc_dir = BASE_DIR / "downloads"
    necc_dir.mkdir(exist_ok=True)
    response = get_response(session, downloads_url)
    soup = BeautifulSoup(response.text, 'lxml')
    table = find_parse(soup, "table", attrs={"class": "docutils"}).find_all("tr")[1:]
    pattern = r'".+\.zip'
    for i in table:
        try:
            zp = find_parse(i, "a", attrs={"href": re.compile(r'.+\.zip')})
            full_url = urljoin(MAIN_DOC_URL, zp.get("href"))
            filename = full_url.split("/")[-1]
            archive_path = necc_dir / filename
            response = session.get(full_url)
            with open(archive_path, 'wb') as file:
                file.write(response.content)
        except Exception as error:
            pass
    logging.info(f"Data downloaded in {necc_dir}")


MODS_OF_WORK = {
    "whats_new": whats_new,
    "latest_versions": latest_versions,
    "download": download
}


def main():
    configure_logging()
    logging.info("Code is running")
    parser = configure_parser(MODS_OF_WORK.keys())
    args = parser.parse_args()
    logging.info(f"Arguments: {args}")
    session = requests_cache.CachedSession()
    if args.clear:
        session.cache.clear()
    mode = args.mode
    visov = MODS_OF_WORK[mode](session)
    if visov is not None:
        control_output(visov, args)
    logging.info("Work is finished")


if __name__ == "__main__":
    main()
