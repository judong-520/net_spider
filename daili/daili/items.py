# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DailiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    country = scrapy.Field()
    agent_ip = scrapy.Field()
    agent_port = scrapy.Field()
    agent_addr = scrapy.Field()
    anonymity = scrapy.Field()
    agent_type = scrapy.Field()
    # 存活时间
    survival_time = scrapy.Field()
    # 验证时间
    verify_time = scrapy.Field()
