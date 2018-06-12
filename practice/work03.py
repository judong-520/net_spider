import robobrowser


def main():
    # 创建浏览器对象
    obj = robobrowser.RoboBrowser(parser='lxml')
    # 通过浏览器加载网页
    obj.open('https://v.taobao.com/v/content/live?catetype=704&from=taonvlang')
    # 获取表单
    form_list = obj.get_form(action='/session')
    # 提交表单
    obj.submit_form(form_list)
    # 筛选带有src属性的img标签
    for img_tag in obj.select('img[src]'):
        print(img_tag.attrs['href'])


if __name__ == '__main__':
    main()


