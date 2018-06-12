from urllib.error import URLError
from urllib.request import urlopen
import re
import pymysql
import ssl

from pymysql import Error


# 通过指定的字符集对页面进行解码(不是每个网站都将字符集设置为utf-8)
def decode_page(page_bytes, charsets=('utf-8',)):
    page_html = None
    for charset in charsets:
        try:
            page_html = page_bytes.decode(charset)
            break
        except UnicodeDecodeError:
            pass
            # logging.error('Decode:', error)
    return page_html


# 获取页面的HTML代码(通过递归实现指定次数的重试操作)
def get_page_html(seed_url, *, retry_times=3, charsets=('utf-8',)):
    page_html = None
    try:
        # urlopen（url） 用于抓取页面，
        # read() 方法用于从文件读取指定的字节数，如果未给定或为负则读取所有。
        page_html = decode_page(urlopen(seed_url).read(), charsets)
    except URLError:
        # logging.error('URL:', error)
        if retry_times > 0:
            return get_page_html(seed_url, retry_times=retry_times - 1,
                                 charsets=charsets)
    return page_html


# 从页面中提取需要的部分(通常是链接也可以通过正则表达式进行指定)
def get_matched_parts(page_html, pattern_str, pattern_ignore_case=re.I):
    pattern_regex = re.compile(pattern_str, pattern_ignore_case)
    return pattern_regex.findall(page_html) if page_html else []


# 开始执行爬虫程序并对指定的数据进行持久化操作
def start_crawl(seed_url, match_pattern, *, max_depth=-1):
    conn = pymysql.connect(host='localhost', port=3306,
                           database='crawler', user='root',
                           password='456654', charset='utf8')
    try:
        with conn.cursor() as cursor:
            url_list = [seed_url]
            visited_url_list = {seed_url: 0}
            while url_list:
                # pop() 函数用于移除列表中的一个元素（默认最后一个元素），并且返回该元素的值。
                current_url = url_list.pop(0)
                depth = visited_url_list[current_url]
                if depth != max_depth:
                    page_html = get_page_html(current_url, charsets=('utf-8', 'gbk', 'gb2312'))
                    links_list = get_matched_parts(page_html, match_pattern)
                    param_list = []
                    for link in links_list:
                        if link not in visited_url_list:
                            visited_url_list[link] = depth + 1
                            page_html = get_page_html(link, charsets=('utf-8', 'gbk', 'gb2312'))
                            headings = get_matched_parts(page_html, r'<h1>(.*)<span')
                            if headings:
                                param_list.append((headings[0], link))
                    cursor.executemany('insert into tb_result values (default, %s, %s)',
                                       param_list)
                    conn.commit()
    except Error:
        pass
        # logging.error('SQL:', error)
    finally:
        conn.close()


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

