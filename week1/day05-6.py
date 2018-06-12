from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def main():
    # 模拟浏览器
    drive = webdriver.Chrome()
    drive.get('https://v.taobao.com/v/content/live?catetype=704&from=taonvlang')
    elem = drive.find_element_by_css_selector('input[placeholder=输入关键词搜索]')
    elem.send_keys('运动')
    elem.send_keys(Keys.ENTER)
    soup = BeautifulSoup(drive.page_source, 'lxml')
    for img_tab in soup.body.select('img[src]'):
        print(img_tab.attrs['src'])


if __name__ == '__main__':
    main()

