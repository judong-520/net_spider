from enum import Enum, unique
from queue import Queue
from random import random
from threading import Thread
from urllib.parse import urlparse, urljoin

import requests
from time import sleep
from bs4 import BeautifulSoup


def main():
    headers = {'user_agent': 'Baiduspider'}
    proxies = {'http': 'http://122.114.31.177:808'}
    base_url = 'https://www.geyanw.com/'
    response = requests.get(base_url, headers=headers, proxies=proxies)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'lxml')
        bs = soup.body.select('a[href]')
        for a_tags in bs:
            print(a_tags)
            print(a_tags.text)
            href = a_tags.attrs['href']
            print(href)
            full_url = urljoin(base_url, href)
            parser = urlparse(full_url)
            sort_html = parser.path.split('/')
            print(parser)
            print(full_url)
            print(parser.path)
            # print(sort_html)
            print('\n')


if __name__ == '__main__':
    main()
