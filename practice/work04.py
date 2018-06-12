from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def main():
    # 创建谷歌浏览器内核
    driver = webdriver.Chrome()
    # 通过谷歌浏览器加载网页（可以加载动态生成的内容）
    driver.get('https://v.taobao.com/v/content/live?catetype=704&from=taonvlang')
    # 通过选择器查找input元素
    elem = driver.find_element_by_css_selector('input[placeholder=输入关键词搜索]')
    # 模拟人为点击事件
    elem.send_keys('运动')
    elem.send_keys(Keys.ENTER)
    # driver.page_source获得的页面, 其页面包含了JavaScript动态创建的内容
    print(driver.page_source)
    # 创建soup对象
    soup = BeautifulSoup(driver.page_source, 'lxml')
    for img_tag in soup.select('img[src]'):
        print(img_tag)


if __name__ == '__main__':
    main()


