def main1():
    a = 1
    b = 1
    for _ in range(20):
        c = a + b
        a = b
        b = c
        print(c)


def fib():
    a, b = 0, 1
    while True:
        a, b = b, a + b
        yield a


def even(gen):
    for val in gen:
        if val % 2 == 0:
            yield val


def main2():
    gen = even(fib())
    for _ in range(10):
        print(next(gen))


def countdown(n):
    while n > 0:
        yield n
        n = n - 1


def main3(n):
    num = countdown(n)
    for _ in range(n):
        # next() 返回迭代器的下一个项目
        print(next(num))


if __name__ == '__main__':
    main1()
    main2()
    main3(5)
