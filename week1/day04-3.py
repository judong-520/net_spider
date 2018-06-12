from urllib.parse import urlparse


def main():
    url = 'http://www.baidu.com/abc/efg/hello?a=b'
    parser = urlparse(url)
    # 协议
    print(parser.scheme)
    # 域名
    print(parser.netloc)
    # 端口
    print(parser.port)
    # 路径
    print(parser.path)
    print(parser.query)
    # scheme = parser.scheme or 'http'
    # netloc = parser.netloc or 'm.sohu.com'
    # path = parser.path
    # query = '?' + parser.query if parser.query else ''
    # url = '%s://%S%S?%S' %(scheme, netloc, path, query)
    # full_url = f'{scheme}://{netloc}{path}{query}'
    str1 = 'hello word!'
    print(str1.index('or'))
    print(str1.find('or'))
    print(str1.find('shit'))
    # print(str1.index('shit'))
    print(str1*5)
    list1 = ['hello']
    print(list1*5)


if __name__ == '__main__':
    main()
