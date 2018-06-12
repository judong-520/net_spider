from urllib.parse import urljoin

import re
import requests

from bs4 import BeautifulSoup


def main():
    # 冒充百度爬虫代理
    headers = {'user-agent': 'Baiduspider'}
    # 代理服务器，隐藏身份
    proxies = {
        'http': 'http://122.114.31.177:808'
    }
    base_url = 'https://www.zhihu.com/'
    print(base_url)
    seed_url = urljoin(base_url, 'explore')
    print(seed_url)
    resp = requests.get(seed_url,
                        headers=headers,
                        proxies=proxies)
    # print(resp.text)
    # 创建BeautifulSoup对象来解析页面
    soup = BeautifulSoup(resp.text, 'lxml')
    # print(soup)
    href_regex = re.compile(r'^/question')
    link_set = set()
    for a_tag in soup.find_all('a', {'href': href_regex}):
        if 'href' in a_tag.attrs:
            href = a_tag.attrs['href']
            full_url = urljoin(base_url, href)
            link_set.add(full_url)
    print('Total %d question pages found.' % len(link_set))


if __name__ == '__main__':
    main()
