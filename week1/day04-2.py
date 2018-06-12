from enum import Enum, unique
from queue import Queue
from threading import Thread
from time import sleep
from random import random
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup


@unique
# 值不能重复
class SpiderStatus(Enum):
    IDLE = 0
    WORKING = 1


# 通过字符集对页面进行解码
def decode_page(page_bytes, charsets=('utf-8',)):
    page_html = None
    for charset in charsets:
        # 拿到的页面可能是空，解码不了，这时候需要捕获错误
        try:
            page_html = page_bytes.decode(charset)
            break
        except UnicodeDecodeError:
            pass
    return page_html


class Retry(object):

    def __init__(self, *, retry_times=3, wait_secs=5, errors=(Exception,)):
        # 默认重试3次，上限时间5秒
        self.retry_times = retry_times
        self.wait_secs = wait_secs
        self.errors = errors

    def __call__(self, fn):

        def wrapper(*args, **kwargs):
            for _ in range(self.retry_times):
                try:
                    return fn(*args, **kwargs)
                except self.errors as e:
                    # logging.error(e)
                    # logging.info('[Retry]')
                    print(e)
                    # random生成（0,1）之间的随机数
                    sleep((random() + 1) * self.wait_secs)
            return None

        return wrapper


class Spider(object):

    def __init__(self):
        self.status = SpiderStatus.IDLE

    # 定义抓取页面，解码方法
    @Retry()
    def fetch(self, current_url, *, charsets=('utf-8',), user_agent=None, proxies=None):
        print('[Fetch]:' + current_url)
        headers = {'user-agent': user_agent} if user_agent else {}
        resp = requests.get(current_url, headers=headers, proxies=proxies)
        html_page = decode_page(resp.content, charsets) if resp.status_code == 200 else None
        return html_page

    # 定义解析页面的方法
    def parse(self, html_page, domain='m.sohu.com'):
        soup = BeautifulSoup(html_page, 'lxml')
        url_links = []
        # soup.body.find_all('a')
        # 找到soup对象中的body中带有href的a标签
        bs = soup.body.select('a[href]')
        for a_tag in bs:
            parser = urlparse(a_tag.attrs['href'])
            # url.parse() 解析url，可以将一个完整的URL地址，分为很多部分，
            # 常用的有：scheme（协议），netloc（域名），port（端口）， path（路径）
            netloc = parser.netloc or domain
            if netloc == domain:
                scheme = parser.scheme or 'http'
                path = parser.path
                query = '?' + parser.query if parser.query else ''
                full_url = f'{scheme}://{netloc}{path}{query}'
                if full_url not in visited_urls:
                    url_links.append(full_url)
        return url_links

    def extract(self, html_page):
        pass

    def store(self, data_dict):
        pass


class SpiderThread(Thread):

    def __init__(self, spider, tasks_queue):
        # daemon守护进程，主程序结束，线程也会结束
        super().__init__(daemon=True)
        self.spider = spider
        # tasks_queue:待处理的页面
        self.tasks_queue = tasks_queue

    def run(self):
        """重写run方法"""
        while True:
            # 拿到当前的url
            current_url = self.tasks_queue.get()
            visited_urls.add(current_url)
            # 如果spider的工作状态为working
            self.spider.status = SpiderStatus.WORKING
            # 抓取当前页面
            html_page = self.spider.fetch(current_url)
            # 如果页面不为空， 解析页面并添加到任务队列中
            if html_page not in [None, '']:
                url_links = self.spider.parse(html_page)
                for url_link in url_links:
                    self.tasks_queue.put(url_link)
            self.spider.status = SpiderStatus.IDLE


def is_any_alive(spider_threads):
    return any([spider_thread.spider.status == SpiderStatus.WORKING for spider_thread in spider_threads])


visited_urls = set()


def main():
    # 任务队列
    task_queue = Queue()  # FIFO先进先出
    # put放东西，放在尾巴上， 只能放一个元素
    task_queue.put('http://m.sohu.com/')
    # 起10个进程
    spider_threads = [SpiderThread(Spider(), task_queue) for _ in range(10)]
    for spider_thread in spider_threads:
        spider_thread.start()
    # 只要队列不为空或者有任何一个蜘蛛存在
    while not task_queue.empty() or is_any_alive(spider_threads):
        pass

    print('Over!')


if __name__ == '__main__':
    main()
