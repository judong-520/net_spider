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

    def process_item(self, item, spider):
        today = time.strptime('%Y%m%d', time.localtime())
        filename = today + '.json'
        with codecs.open(filename, 'a', encoding='utf-8') as fp:
            line = json.dumps(dict(item), ensure_ascii=False) + '\n'
            fp.write(line)
        return item