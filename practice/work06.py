from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def main():
    base_url = 'http://sports.sohu.com/'
    response = requests.get('http://sports.sohu.com/nba_a.shtml')
    decode_html = response.content.decode('gbk')
    soup_obj = BeautifulSoup(decode_html, 'lxml')
    a_tags = soup_obj.select('a[href]')
    count = 0
    all_url = set()
    for a_tag in a_tags:
        count += 1
        full_url = urljoin(base_url, a_tag['href'])
        # full_url = urljoin(a_tag['href'], base_url)
        print(full_url)
        all_url.add(full_url)
    print(count)
    print(len(all_url))


if __name__ == '__main__':
    main()
