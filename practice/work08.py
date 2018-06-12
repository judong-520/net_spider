from enum import unique, Enum

import time
from queue import Queue
from threading import Thread
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


visited_urls = set()


@unique
class SpiderStatus(Enum):
    IDEL = 0
    WORKING = 1


def decode_page(page_bytes, charsets=('utf-8',)):
    page_html = None
    for charset in charsets:
        try:
            page_html = page_bytes.decode(charset)
        except UnicodeDecodeError:
            pass
    return page_html


class Retry(object):

    def __init__(self, *, retry_times=3, wait_secs=3, errors=(Exception,)):
        self.retry_times = retry_times
        self.wait_secs = wait_secs
        self.errors = errors

    def __call__(self, fn):
        # Python中类的实例（对象）可以被当做函数对待。
        # 也就是说，我们可以将它们作为输入传递到其他的函数方法中并调用他们，
        # 正如我们调用一个正常的函数那样。而类中__call__()函数的意义正在于此。

        def wrapper(*args, **kwargs):
            for _ in range(self.retry_times):
                try:
                    return fn(*args, **kwargs)
                except self.errors:
                    pass
                time.sleep(self.wait_secs)
            return None
        return wrapper


class Spider(object):

    def __init__(self):
        self.status = SpiderStatus.IDEL

    @Retry()
    def fetch(self, current_url, *, charsets=('utf-8',), user_agent=None, proxies=None):
        print('[Fetch]:' + current_url)
        headers = {'user_agent': user_agent} if user_agent else {}
        resp = requests.get(current_url, headers=headers, proxies=proxies)
        html_page = decode_page(resp.content, charsets) if resp.status_code == 200 else None
        return html_page

    def parse(self, html_page):
        soup = BeautifulSoup(html_page, 'lxml')
        url_links = []
        base_url = 'http://sports.sohu.com/'
        a_tags = soup.body.select('a[href]')
        for a_tag in a_tags:
            href = a_tag.attrs['href']
            full_url = urljoin(base_url, href)
            if full_url not in visited_urls:
                url_links.append(full_url)
        return url_links


class SpiderThread(Thread):

    def __init__(self, spider, task_queue):
        super().__init__(daemon=True)
        self.spider = spider
        self.task_queue = task_queue

    def run(self):
        while True:
            current_url = self.task_queue.get()
            visited_urls.add(current_url)
            self.spider.status = SpiderStatus.WORKING
            html_page = self.spider.fetch(current_url)
            if html_page not in ['', None]:
                url_links = self.spider.parse(html_page)
                for url_link in url_links:
                    self.task_queue.put(url_link)
            self.spider.status = SpiderStatus.IDEL


def is_any_alive(spider_threads):
    return any([spider_thread.spider.status == SpiderStatus.WORKING for spider_thread in spider_threads])


def main():
    task_queue = Queue()
    # put放东西，放在尾巴上， 只能放一个元素
    task_queue.put('http://m.sohu.com/')
    spider_threads = [SpiderThread(Spider(), task_queue) for _ in range(10)]
    for spider_thread in spider_threads:
        spider_thread.start()
    while not task_queue.empty() or is_any_alive(spider_threads):
        pass

    print('Over!')


if __name__ == '__main__':
    main()



