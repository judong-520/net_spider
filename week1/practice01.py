from urllib.parse import urljoin
from urllib.request import urlopen

from bs4 import BeautifulSoup


def main():
    visited_urls = set()
    decode_html = None
    # 用户代理
    # header = {'user-agent': 'Baudupider'}
    # 服务器代理
    # proxies = {'http': 'http://122.114.31.177:808'}
    # 设置基本页面
    base_html = 'http://sports.sohu.com/nba_a.shtml'
    # 抓取页面
    get_html = urlopen(base_html)
    # 读取页面， 输出的数据是byte类型
    read_html = get_html.read()
    # 页面解码
    charsets = ['utf-8', 'gbk', 'gb2312']
    for charset in charsets:
        try:
            decode_html = read_html.decode(charset)
        except UnicodeDecodeError:
            pass
    # 生成BeautifulSoup对象
    soup_html = BeautifulSoup(decode_html, 'lxml')
    # 在BeautifulSoup对象的<body>中挑选有href属性的<a>标签
    a_tags = soup_html.body.select('a[href]')
    counter = 0
    for a_tag in a_tags:
        counter += 1
        url_href = a_tag.attrs['href']
        full_url = urljoin(base_html, url_href)
        visited_urls.add(full_url)
    print(visited_urls)
    print(counter)
    print(len(visited_urls))


if __name__ == '__main__':
    main()

# append()方法用于在列表末尾添加新的对象。
# add()方法用于在集合添加新对象

