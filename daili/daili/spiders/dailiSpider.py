# -*- coding: utf-8 -*-
import scrapy
from urllib import parse

from daili.items import DailiItem


class DailispiderSpider(scrapy.Spider):
    name = 'dailiSpider'
    allowed_domains = ['xicidaili.com']
    start_urls = ['http://www.xicidaili.com/']

    def parse(self, response):
        item = DailiItem()
        base_url = 'http://www.xicidaili.com/'
        tr_list = response.xpath('//*[@id="ip_list"]//tr')
        # tr_list = response.xpath('//*[@id="ip_list"]//tbody/tr')
        for tr in tr_list:
            # href = li.xpath('h6/a/@href').extract_first()
            tr_class = tr.xpath('@class').extract_first()
            if tr_class == '' or tr_class == 'odd':
                item['country'] = tr.xpath('td[1]/img/@src').extract_first()
                item['agent_ip'] = tr.xpath('td[2]/text()').extract_first()
                item['agent_port'] = tr.xpath('td[3]/text()').extract_first()
                item['agent_addr'] = tr.xpath('td[4]/text()').extract_first()
                item['anonymity'] = tr.xpath('td[5]/text()').extract_first()
                item['agent_type'] = tr.xpath('td[6]/text()').extract_first()
                item['survival_time'] = tr.xpath('td[7]/text()').extract_first()
                item['verify_time'] = tr.xpath('td[8]/text()').extract_first()
                yield item
            elif tr_class == None:
                a_href = tr.xpath('th/a/@href').extract_first()
                url = parse.urljoin(base_url, a_href)
                # url =response.urljoin(a_href)
                yield scrapy.Request(url=url, callback=self.parse)
            else:
                pass
