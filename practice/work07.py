from hashlib import sha1
from urllib.parse import urljoin

import re

import pickle
import redis
import requests
import zlib
from bs4 import BeautifulSoup


def main():
    headers = {'user-agent': 'Baiduspider'}
    proxies = {'http': 'http://122.114.31.177:808'}
    join_url = urljoin('https://www.zhihu.com/', '/explore')
    get_url = requests.get(join_url, headers=headers, proxies=proxies)
    decode_html = get_url.content.decode('utf-8')
    soup_obj = BeautifulSoup(decode_html, 'lxml')
    href_regex = re.compile(r'^/question')
    a_tags = soup_obj.find_all('a', {'href': href_regex})
    base_hrefs = set()
    for a_tag in a_tags:
        all_href = a_tag.attrs['href']
        full_hrefs = urljoin('https://www.zhihu.com/', all_href)
        base_hrefs.add(full_hrefs)
    print(base_hrefs)
    redis_client = redis.Redis(host='47.98.173.29', port=6379, password=123456)
    # 将url处理成sha1摘要
    hashe_proto = sha1()
    # 传入url生成sha1摘要
    hasher = hashe_proto.copy()
    field_key = hasher.hexdigest()
    for base_href in base_hrefs:
        hasher.update(base_href.encode('utf-8'))
        print(base_href)
        if not redis_client.hexists('zhihu', field_key):
            html_page = requests.get(base_href, headers=headers).text
            zipped_page = zlib.compress(pickle.dumps(html_page))
            redis_client.hset('zhihu', field_key, zipped_page)
    print('Total %d question pages found.' % redis_client.hlen('zhihu'))


if __name__ == '__main__':
    main()


# hash.digest()
# 返回摘要，作为二进制数据字符串值
# hash.hexdigest()
# 返回摘要，作为十六进制数据字符串值
