import robobrowser


def main():
    # 创建浏览器对象
    obj = robobrowser.RoboBrowser(parser='lxml')
    # 传递网页
    obj.open('https://github.com/login')
    # 获取表单
    form = obj.get_form(action='/session')
    form['login'].value = 'judong-520'
    form['password'].value = 'ab456654'
    obj.submit_form(form)
    for a_tag in obj.select('a[href]'):
        print(a_tag)


if __name__ == '__main__':
    main()
