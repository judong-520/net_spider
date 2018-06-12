# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy import log
from scrapy.conf import settings
from scrapy.exceptions import DropItem


class DoubanPipeline(object):

    def __init__(self):
        self.mongo_client = pymongo.MongoClient(host='47.98.173.29', port=27017)
        self.db = self.mongo_client.douban
        self.connection = self.db.movie

    def process_item(self, item, spider):
        self.connection.insert(dict(item))
        return item

