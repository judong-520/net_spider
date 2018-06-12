# -*- coding: utf-8 -*-
import scrapy
from urllib import parse

from tianqi.items import TianqiItem


class TianqispiderSpider(scrapy.Spider):
    name = 'tianqiSpider'
    allowed_domains = ['m.tianqi.com']
    base_url = 'https://m.tianqi.com'
    start_urls = ['https://m.tianqi.com/longquanyi/']

    def parse(self, response):
        item = TianqiItem()
        item['area'] = response.xpath('/html/body/div[2]/div[2]/h2/text()').extract_first()
        item['wind'] = response.xpath('/html/body/div[2]/div[4]/div[2]/span[3]/text()').extract_first()
        dl_list = response.xpath('/html/body/div[2]/div[5]/dl')
        # '/html/body/div[2]/div[5]/dl[1]/dd[4]/b'
        for dl in dl_list:
            item['date'] = dl.xpath('dd[1]/text()').extract_first()
            item['img'] = dl.xpath('dd[2]/img/@src').extract_first()
            item['weather'] = dl.xpath('dd[3]/text()').extract_first()
            item['temperature'] = dl.xpath('dd[4]/text()').extract_first() + dl.xpath('dd[4]/b/text()').extract_first() + '°C'
            yield item

        li_list = response.xpath('/html/body/div[2]/ul[1]/li')
        for li in li_list:
            href = li.xpath('h6/a/@href').extract_first()
            url = response.urljoin(href)
            # url = parse.urljoin(self.base_url, href)
            yield scrapy.Request(url=url, callback=self.parse)




