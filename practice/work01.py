import requests
from bs4 import BeautifulSoup


def main():
    # 获取页面
    resp = requests.get('https://github.com/login')
    if resp.status_code != 200:
        return
    # 获取cookies
    cookies = resp.cookies.get_dict()
    print(cookies)
    # html = resp.content.decode('gbk')
    # 创建BeautifulSoup对象来解析页面(相当于JavaScript的DOM)
    # bs = BeautifulSoup(html, 'lxml')

    # 创建soup对象
    soup = BeautifulSoup(resp.text, 'lxml')
    # print(type(soup.select('form input[name=utf8]')))
    # print(type(soup.select_one('form input[name=utf8]')))
    # select返回的是列表，selec_one返回的是对象

    # 筛选有value属性的form中的input标签
    utf8_value = soup.select_one('form input[name=utf8]').attrs['value']
    authenticity_token_value = soup.select_one('form input[name=authenticity_token]').attrs['value']
    data ={
        'utf8': utf8_value,
        'authenticity_token': authenticity_token_value,
        'login': 'judong-520',
        'password': 'ab456654'
    }
    response = requests.post('https://github.com/session', data=data, cookies=cookies)
    print(response.text)


if __name__ == '__main__':
    main()

