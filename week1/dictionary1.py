def foo():
    scores = {'骆昊': 95, '白元芳': 78, '狄仁杰': 82}
    # 通过键可以获取字典中对应的值
    print(scores['骆昊'])
    print(scores['狄仁杰'])
    # 对字典进行遍历(遍历的其实是键再通过键取对应的值)
    for elem in scores:
        print('%s\t--->\t%d' % (elem, scores[elem]))
    # 更新字典中的元素
    scores['白元芳'] = 65
    scores['诸葛王朗'] = 71
    scores.update(冷面=67, 方启鹤=85)
    print(scores)
    if '武则天' in scores:
        print(scores['武则天'])
    print(scores.get('武则天'))
    # get方法也是通过键获取对应的值但是可以设置默认值
    print(scores.get('武则天', 60))
    # 删除字典中的元素
    print(scores.popitem())
    print(scores.popitem())
    print(scores.pop('骆昊', 100))
    # 清空字典
    scores.clear()
    print(scores)


if __name__ == '__main__':
    foo()
    

"""

题目8: 设计一个函数，统计一个字符串中出现频率最高的字符及其出现次数

"""


def find_most_freq(string):
    result_dict = {}
    for ch in string:
        if ch in result_dict:
            result_dict[ch] += 1
        else:
            result_dict[ch] = 1
    max_keys = []
    max_value = 0
    for key, value in result_dict.items():
        if value > max_value:
            max_value = value
            max_keys.clear()
            max_keys.append(key)
        elif value == max_value:
            max_keys.append(key)
    return max_keys, max_value


def main():
    print(find_most_freq('aabbaaccbb'))  # (['a', 'b'], 4)
    print(find_most_freq('hello, world!'))  # (['l'], 3)
    print(find_most_freq('a1bb2ccc3aa'))  # (['a', 'c'], 3)


if __name__ == '__main__':
    main()
