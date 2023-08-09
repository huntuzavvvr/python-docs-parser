import re
from urllib.parse import urljoin
import requests_cache
from tqdm import tqdm
from bs4 import BeautifulSoup
from constants import BASE_DIR, MAIN_DOC_URL
from configs import configure_parser
from outputs import *

def whats_new(session):
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    response = session.get(whats_new_url)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, 'lxml')
    sect = soup.find("section", attrs={"id": "what-s-new-in-python"})
    l1 = sect.find("div").find_all(class_="toctree-l1")
    results = [("Link to docs", "Name", "Author/Editor")]
    for i in tqdm(l1):
        a = i.find("a")
        href = a.get("href")
        full_link = urljoin(whats_new_url, href)
        # print(full_link)
        session = requests_cache.CachedSession()
        response = session.get(full_link)
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, 'lxml')
        sec = soup.find("section")
        title = sec.find("h1").text
        descr = sec.find("dl").text
        descr = descr.replace("\n", ' ')
        results.append((full_link, title, descr))
    # for result in results:
    #     print(*result)
    # control_output(results, args)
    return results


def latest_versions(session):
    response = session.get(MAIN_DOC_URL)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "lxml")
    links = soup.find("div", class_="sphinxsidebarwrapper").find("ul")
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
        # Печать результата.
    return results


def download(session):
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    necc_dir = BASE_DIR / "downloads"
    necc_dir.mkdir(exist_ok=True)
    response = session.get(downloads_url)
    soup = BeautifulSoup(response.text, 'lxml')
    table = soup.find("table", class_="docutils").find_all("tr")[1:]
    pattern = r'".+\.zip'
    for i in tqdm(table):
        try:
            zp = i.find("a", attrs={"href": re.compile(r'.+\.zip')})
            full_url = urljoin(downloads_url, zp.get("href"))
            filename = full_url.split("/")[-1]
            archive_path = necc_dir / filename
            response = session.get(full_url)
            with open(archive_path, 'wb') as file:
                file.write(response.content)
        except Exception as error:
            pass


MODS_OF_WORK = {
    "whats_new": whats_new,
    "latest_versions": latest_versions,
    "download": download
}


def main():
    parser = configure_parser(MODS_OF_WORK.keys())
    args = parser.parse_args()
    session = requests_cache.CachedSession()
    if args.clear:
        session.cache.clear()
    mode = parser.parse_args().mode
    visov = MODS_OF_WORK[mode](session)
    if visov is not None:
        control_output(visov, args)


if __name__ == "__main__":
    main()
