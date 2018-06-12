import requests
from bs4 import BeautifulSoup


def main():
    # 获取页面
    resp = requests.get('https://github.com/login')
    # print(resp.content)
    # print('____________________________________________________________________________________________________')
    # print('\n')
    # print(resp.text)
    # print('____________________________________________________________________________________________________')
    if resp.status_code != 200:
        return
    # 从页面中取cookie
    cookies = resp.cookies.get_dict()
    # print(cookies)
    soup = BeautifulSoup(resp.text, 'lxml')
    utf8_value = soup.select_one('form input[name=utf8]').attrs['value']
    authenticity_token = soup.select_one('form input[name=authenticity_token]').attrs['value']
    data = {
        'utf8': utf8_value,
        'authenticity_token': authenticity_token,
        'login': 'judong-520',
        'password': 'ab456654'
    }
    # files ={
    #     'files1': open(),
    #     'files2': open(),
    #     'files3': open(),
    # }
    resp = requests.post('https://github.com/session', data=data, cookies=cookies)
    print(resp.text)


if __name__ == '__main__':
    main()
