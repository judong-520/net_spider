import requests
import robobrowser


def main():
    # resp = requests.get('https://github.com/login')
    # 创建浏览器对象
    b = robobrowser.RoboBrowser(parser='lxml')
    b.open('https://github.com/login')
    # 拿到表单
    f = b.get_form(action='/session')
    f['login'].value = 'judong-520'
    f['password'].value = 'ab456654'
    b.submit_form(f)
    for a_tag in b.select('a[href]'):
        print(a_tag.attrs['href'])

    # # 创建浏览器对象
    # b = robobrowser.RoboBrowser(parser='lxml')
    # b.open('https://v.taobao.com/v/content/live?catetype=704&from=taonvlang')
    # # 拿到表单
    # print(b)
    # f = b.get_form(action='/session')
    # b.submit_form(f)
    # for img_tag in b.select('img[src]'):
    #     print(img_tag.attrs['href'])


if __name__ == '__main__':
    main()
