# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json
import pymongo
import time
import os
# import urllib
from urllib.request import urlopen


class TianqiPipeline(object):

    # 保存在MongoDB中
    def __init__(self):
        self.mongo_client = pymongo.MongoClient(host='47.98.173.29', port=27017)
        self.db = self.mongo_client.tianqi
        self.connction = self.db.chengdu

    def process_item(self, item, spider):
        self.connction.insert(dict(item))
        return item

    # 保存在.txt文档中
    # def process_item(self, item, spider):
    #     today = time.strftime('%Y%m%d', time.localtime())
    #     filename = today + '.txt'
    #     with open(filename, 'a', encoding='utf-8') as fp:
    #         fp.write(item['area'] + '\t')
    #         fp.write(item['date'] + '\t')
    #         fp.write(item['wind'] + '\t')
    #         fp.write(item['temperature'] + '\t')
    #         imgname = os.path.basename(item['img'])
    #         fp.write(imgname + '\t')
    #         if os.path.exists(imgname):
    #             pass
    #         else:
    #             with open(imgname, 'wb') as fp:
    #                 response = urlopen(item['img'])
    #                 fp.write(response.read())
    #         fp.write(item['date'] + '\t')
    #         fp.write(item['weather'] + '\n\n')
    #         time.sleep(1)
    #     return item

    # 保存在.json文档中
    # def process_item(self, item, spider):
    #     today = time.strftime('%Y%m%d', time.localtime())
    #     filename = today + '.json'
    #     with codecs.open(filename, 'a', encoding='utf-8') as fp:
    #         line = json.dumps(dict(item), ensure_ascii=False) + '\n'
    #         fp.write(line)
    #     return item
