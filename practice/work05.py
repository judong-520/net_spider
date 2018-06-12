import ssl
from urllib.error import URLError
from urllib.request import urlopen

import re

import pymysql
from pymysql import Error


def decode_page(page_bytes, charsets=('utf-8', )):
    page_html = None
    for charset in charsets:
        try:
            # 对字节解码
            page_html = page_bytes.decode(charset)
            break
        except UnicodeDecodeError:
            pass
    return page_html


def get_page_html(seed_url, *, retry_times=3, chatsets=('utf-8',)):
    page_html = None
    try:
        # 获取页面
        get_html = urlopen(seed_url)
        # 对页面进行读取，得到的是字节数据
        read_html = get_html.read()
        page_html = decode_page(read_html, charsets=('utf-8',))
    except URLError:
        if retry_times > 0:
            return get_page_html(seed_url, retry_times=retry_times-1, chatsets=chatsets)
    return page_html


# 从页面提取需要的部分，通过正则表达式进行指定
def get_matched_parts(page_html, pattern_str, pattern_ignore_case=re.I):
    pattern_regex = re.compile(pattern_str, pattern_ignore_case)
    # 正则表达式返回的是列表
    return pattern_regex.findall(page_html) if page_html else []


# 执行爬虫程序，并对有效数据进行持久化操作
def start_crawl(seed_url, match_pattern, *, max_depth=-1):
    connect = pymysql.connect(host='localhost', port=3306,
                              database='crawler', user='root',
                              password='456654', charset='utf8')
    try:
        with connect.cursor() as cursor:
            url_list = [seed_url]
            visited_url_list = {seed_url: 0}
            while url_list:
                # pop() 函数用于移除列表中的一个元素（默认最后一个元素），并且返回该元素的值。
                current_url = url_list.pop(0)
                depth = visited_url_list[current_url]
                if depth != max_depth:
                    page_html = get_page_html(current_url, chatsets=('utf-8', 'gbk', 'gb2312'))
                    links_list = get_matched_parts(page_html, match_pattern)
                    param_list = []
                    for link in links_list:
                        if link not in visited_url_list:
                            visited_url_list[link] = depth + 1
                            page_html = get_page_html(link, chatsets=('utf-8', 'gbk', 'gb2312'))
                            heading = get_matched_parts(page_html, r'<h1>(.*)<span')
                            if heading:
                                param_list.append((heading[0], link))
                    cursor.executemany('insert into tb_result values (default, %s, %s)', param_list)
                    connect.commit()
    except Error:
        pass
    finally:
        connect.close()


def main():
    ssl._create_default_https_context = ssl._create_unverified_context
    start_crawl('http://sports.sohu.com/nba_a.shtml',
                r'<a[^>]+test=a\s[^>]*href=["\'](.*?)["\']',
                max_depth=2)


if __name__ == '__main__':
    main()


# urlopen(url, data=None, proxies=None)
#     Create a file-like object for the specified URL to read from.
# 即创建一个类文件对象为指定的 url 来读取。
# 详细点就是，创建一个表示远程url的类文件对象，然后像本地文件一样操作这个类文件对象来获取远程数据。参数url表示远程数据的路径，一般是网址;参数data表示以post方式提交到url的数据(玩过web的人应该知道提交数据的两种方式：post与get。如果你不清楚，也不必太在意，一般情况下很少用到这个参数);参数proxies用于设置代理(这里不详细讲怎么使用代理，感兴趣的看客可以去翻阅Python手册urllib模块)。 urlopen返回 一个类文件对象，他提供了如下方法：
# 参数 url 表示远程数据的路径，一般是 http 或者 ftp 路径。
# 参数 data 表示以 get 或者 post 方式提交到 url 的数据。
# 参数 proxies 表示用于代理的设置。
# urlopen 返回一个类文件对象，它提供了如下方法：
# read() , readline() , readlines()，fileno()和close()： 这些方法的使用与文件对象完全一样。

