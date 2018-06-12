from urllib.parse import urljoin

import re
import requests
from bs4 import BeautifulSoup


def main():
    page_text = None
    base_url = 'https://www.hao123.com'
    resp = requests.get(base_url)
    if resp.status_code == 200:
        try:
            page_text = resp.content.decode('utf-8')
        except UnicodeDecodeError:
            pass
    else:
        return
    soup = BeautifulSoup(page_text, 'lxml')
    a_tages = soup.select('a[href]')
    url_links = set()
    for a_tage in a_tages:
        href = a_tage.attrs['href']
        full_href = urljoin(base_url, href)
        if 'http' in full_href or 'https' in full_href:
            url_links.add(full_href)
    print(url_links)


if __name__ == '__main__':
    main()

