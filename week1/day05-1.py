from enum import Enum, unique
from queue import Queue
from random import random
from threading import Thread
from urllib.parse import urlparse

import requests
import logging
from time import sleep
from bs4 import BeautifulSoup


@unique
class SpiderStatus(Enum):
    IDLE = 0
    WORKING = 1


def decode_page(page_bytes, charsets=('utf-8',)):
    page_html = None
    for charset in charsets:
        try:
            page_html = page_bytes.decode(charset)
            break
        except UnicodeDecodeError:
            pass
    return page_html


def is_any_alive(spider_threads):
    return any([spider_thread.spider.status == SpiderStatus.WORKING for spider_thread in spider_threads])


class Retry(object):

    # 传入*，表示*之后必须是关键字参数, (传参)关键字参数可以不和定义参数的顺序写，大三室必须把关键字加上
    def __int__(self, *, retry_times=3, wait_secs=5, errors=(Exception,)):
        self.retry_tmes = retry_times
        self.wait_secs = wait_secs
        self.errors = errors

    def __call__(self, fn):

        # 不知道要传什么参数的时候用*args, **kwargs
        # 多个实参，放到一个元组里面, 以 * 开头，可以传多个参数；
        # ** 是形参中按照关键字传值把多余的传值以字典的方式呈现
        # *args：（表示的就是将实参中按照位置传值，多出来的值都给args，且以元祖的方式呈现）
        def wrappper(*args, **kwargs):
            for _ in range(self.retry_tmes):
                try:
                    return fn(*args, **kwargs)
                except self.errors as e:
                    print(e)
                    sleep((random() + 1) * self.wait_secs)
            return None
        return wrappper


class Spider(object):

    def __init__(self):
        self.status = SpiderStatus.IDLE

    # 抓取页面，并返回解码的页面
    def fetch(self, current_url, *, charsets=('utf-8',), user_agent=None, proxies=None):
        print('[Fetch]: ' + current_url)
        headers = {'user_agent': user_agent} if user_agent else {}
        response = requests.get(current_url, headers=headers, proxies=proxies)
        decode_resp = decode_page(response.content, charsets) if response.status_code == 200 else None
        return decode_resp

    # 解析页面，将可用的数据信息存储在集合中
    def parse(self, html_page, *, domain='www.geyanw.com'):
        url_links = []
        soup = BeautifulSoup(html_page, 'lxml')
        bs = soup.body.select('a[href]')
        for a_tag in bs:
            # url.parse() 解析url，可以将一个完整的URL地址，分为很多部分，
            # 常用的有：scheme（协议），netloc（域名），port（端口）， path（路径）
            parser = urlparse(a_tag.attrs['href'])
            # 域名
            netloc = parser.netloc or domain
            if netloc == domain:
                scheme = parser.scheme or 'https'
                path = parser.path
                query = '?' + parser.query if parser.query else ''
                full_url = f'{scheme}://{netloc}{path}{query}'
                if full_url not in visited_urls:
                    url_links.append(full_url)
        return url_links


class SpiderThread(Thread):

    def __init__(self, spider, tasks_queue):
        super().__init__(daemon=True)
        self.spider = spider
        self.tasks_queue = tasks_queue

    def run(self):
        while True:
            current_url = self.tasks_queue.get()
            visited_urls.add(current_url)
            self.spider.status = SpiderStatus.WORKING
            html_page = self.spider.fetch(current_url)
            if html_page not in [None, '']:
                url_links = self.spider.parse(html_page)
                for url_link in url_links:
                    self.tasks_queue.put(url_link)
            self.spider.status = SpiderStatus.IDLE


visited_urls = set()


def main():
    task_queue = Queue()
    task_queue.put('https://www.geyanw.com/')
    spider_threads = [SpiderThread(Spider(), task_queue) for _ in range(10)]
    for spider_thread in spider_threads:
        spider_thread.start()
    while not task_queue.empty() or is_any_alive(spider_threads):
        pass
    print('Over!')


if __name__ == '__main__':
    main()



