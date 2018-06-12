# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
import os
import pymongo
import time
from urllib import request


class DailiPipeline(object):

    #在MongoDB中持久化操作
    # def __init__(self):
    #     self.mongo_client = pymongo.MongoClient(host='47.98.173.29', port=27017)
    #     self.db = self.mongo_client.daili
    #     self.connection = self.db.agent
    #
    # def process_item(self, item, spider):
    #     self.connection.insert(dict(item))
    #     return item

    # def process_item(self, item, spider):
    #     now = time.strftime('%Y%m%d', time.localtime())
    #     filename = 'Daili' + now + '.txt'
    #     with open(filename, 'a', encoding='utf-8') as fp:
    #         # 按照下载的路径存储的
    #         imgname = os.path.basename(item['country'])
    #         fp.write(imgname + ' ')
    #         if os.path.exists(imgname):
    #             pass
    #         else:
    #             with open(imgname, 'wb') as fp:
    #                 response = request.urlopen(item['country'])
    #                 fp.write(response.read())
    #         fp.write(item['agent_ip'] + ' ')
    #         fp.write(item['agent_port'] + ' ')
    #         fp.write(item['agent_addr'] + ' ')
    #         fp.write(item['anonymity'] + ' ')
    #         fp.write(item['agent_type'] + ' ')
    #         fp.write(item['survival_time'] + ' ')
    #         fp.write(item['verify_time'] + '\n\n')
    #         time.sleep(1)
    #     return item

    def process_item(self, item, spider):
        now = time.strftime('%Y%m%d', time.localtime())
        filename = 'Daili' + now + '.json'
        with codecs.open(filename, 'a', encoding='utf-8') as fp:
            line = json.dumps(dict(item), ensure_ascii=False) + '\n'
            fp.write(line)
        return item
