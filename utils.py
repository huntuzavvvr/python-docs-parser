import logging
from requests import RequestException
from exception import FindingException


def get_response(session, url):
    try:
        response = session.get(url)
        response.encoding = 'utf-8'
        return response
    except RequestException as error:
        logging.exception(f"Exception {url}", stack_info=True)


def find_parse(soup, tag, attrs=None):
    result = soup.find(tag, attrs=(attrs or {}))
    if not result:
        logging.error(f"Not found {tag}-{attrs}", stack_info=True)
        raise FindingException(f"Not found {tag}-{attrs}")
    return result