from time import sleep
from inspect import getgeneratorstate


def countdown_gen(n, consumer):
    print(getgeneratorstate(consumer))
    # 预先激活消费者
    # consumer.send(None)
    # 所谓的激活就是让代码执行到yield表达式
    next(consumer)
    print(getgeneratorstate(consumer))
    while n > 0:
        consumer.send(n)
        n -= 1
    # consumer.send(None)
    # try:
    #     consumer.send(None)
    # except StopIteration:
    #     pass
    # consumer.close()
    # print(getgeneratorstate(consumer))


def countdown_con():
    while True:
        n = yield
        print('Countdown:', n)
        sleep(1)
        # if n:
        #     print('Countdown:', n)
        #     sleep(1)
        # else:
        #     break


def main():
    consumer = countdown_con()
    countdown_gen(5, consumer)


if __name__ == '__main__':
    main()
