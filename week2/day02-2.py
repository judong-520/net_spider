# 过滤（需要筛选的数据） -> 映射（把数据映射成想要的形式） -> 规约


def add(num_list):
    result = num_list[0]
    for index in range(1, len(num_list)):
        result += num_list[index]


def mul(num_list):
    result = num_list[0]
    for index in range(1, len(num_list)):
        result *= num_list[index]


def calc(num_list, fn):
    result = num_list[0]
    for index in range(1, len(num_list)):
        result = fn(result, num_list[index])
    return result


def add1(x, y):
    return x + y


def main():
    my_list = [1, 2, 3, 4, 5]
    print(calc(my_list, add1))
    print(calc(my_list, lambda x, y: x + y))
    thy_list = [45, 96, 32, 77, 68, 53, 18]
    print(calc(thy_list,add1))


if __name__ == '__main__':
    main()
