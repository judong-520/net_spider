import asyncio
import aiohttp

import requests
import time


@asyncio.coroutine
async def download1(url):
    # 异步执行 - 非阻塞式
    # await asyncio.sleep(1)
    # 同步执行 - 阻塞式
    time.sleep(1)


@asyncio.coroutine
def download(url):
    print('Fetch:', url)
    yield from asyncio.sleep(0.1)
    time.sleep(1)
    # requests是同步请求
    resp = requests.get(url)
    print(url, '-->', resp.status_code)
    print(url, '-->', resp.headers)
    print(url, '-->', resp.cookies)
    # print(resp.text)
    # return resp.status_code, resp.headers


def main():
    loop = asyncio.get_event_loop()
    # 异步i/o，虽然只有一个线程但是2个任务之间不阻塞
    urls = [
        'https://www.baidu.com',
        'http://www.sohu.com',
        'http://www.sina.com',
        'https://www.taobao.com',
        'http://www.qq.com'
    ]
    tasks = [download(url) for url in urls]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()


if __name__ == '__main__':
    main()
