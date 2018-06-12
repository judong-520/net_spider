from random import randint, randrange
from time import sleep

from myutils.wrapper import coroutine


@ coroutine
def create_delivery_man(name, capacity=1):
    buffer = []
    while True:
        size = 0
        while size < capacity:
            # 等待生成器传递包裹
            pkg_name = yield
            if pkg_name:
                size += 1
                buffer.append(pkg_name)
                print('%s正在接收%s' % (name, pkg_name))
            else:
                break
        print('%s正在派送%d件包裹' % (name, len(buffer)))
        sleep(3)
        buffer.clear()


def create_package_center(consumers, max_packages):
    # 预激活消费者
    # consumer.send(None)
    num = 0
    while num <= max_packages:
        print('快递中心准备派送%d号包裹')
        index = randrange(len(consumers))
        consumers[index].send('包裹-%d' % num)
        num += 1
        if num % 10 == 0:
            sleep(10)
    for consumer in consumers:
        consumer.send(None)


def main():
    dm1 = create_delivery_man('八神庵', 10)
    dm2 = create_delivery_man('草薙京', 9)
    create_package_center([dm1, dm2], 22)


if __name__ == '__main__':
    main()
