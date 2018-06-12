from urllib.request import urlopen

from bs4 import BeautifulSoup

url = 'http://sports.sohu.com/nba_a.shtml'
print(url)
print(urlopen(url))
print(urlopen(url).read())
print(urlopen(url).read().decode('gbk'))
html = urlopen(url).read().decode('gbk')
bs = BeautifulSoup(html, 'lxml')
print('-------------------------我是分割线----------------------------')
print(bs)





