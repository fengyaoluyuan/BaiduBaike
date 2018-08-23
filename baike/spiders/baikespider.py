# -*- coding: utf-8 -*-
from scrapy import Request, Spider
import random
import time
from baike.items import BaikeItem

class BaikeSpider(Spider):
    name = 'baikespider'
    allowed_domains = ['baike.baidu.com']
    base_urls = 'http://baike.baidu.com/'

    def __init__(self, keyword, headers):
        self.keyword = keyword
        self.headers = headers
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            keyword=crawler.settings.get('KEYWORD'),
            headers=crawler.settings.get('DEFAULT_REQUEST_HEADERS')
        )

    def start_requests(self):
        for word in self.keyword:
            search_url = self.base_urls + word
            yield Request(url=search_url, callback=self.parse_index, headers=self.headers, dont_filter=True)

    def parse_index(self, response):
        fenlei_url = response.xpath('.//a[contains(@href, "http://baike.baidu.com/fenlei/")]/@href').extract()
        for single_url in fenlei_url:
            yield Request(url=single_url, callback=self.parse_search, headers=self.headers, dont_filter=True)
            time.sleep(random.random())

    def parse_search(self, response):
        title_list = response.xpath('.//a[contains(@href, "view")]/text()').extract()
        #提取当页链接
        for title in title_list:
            article_url = 'https://baike.baidu.com/item/{title}'.format(title=title)
            yield Request(url=article_url, callback=self.parse_details, headers=self.headers, dont_filter=True)
            time.sleep(random.random())
        #提取下一页链接
        if response.xpath('.//a[@id="next" and contains(., "下一页")]//@href').extract():
            next_url = response.xpath('.//a[@id="next" and contains(., "下一页")]//@href').extract()[0]
            next_page_url = 'http://baike.baidu.com/fenlei/{next_url}'.format(next_url=next_url)
            print("当前连接：", next_page_url)
            yield Request(url=next_page_url, callback=self.parse_search, headers=self.headers, dont_filter=True)
        else:
            pass

    def parse_details(self, response):
        if response.status == 200:
            # url = response.url
            title = response.xpath('.//dd[@class="lemmaWgt-lemmaTitle-title"]/h1/text()').extract()[0]
            print(title)
            baike_item = BaikeItem()
            for field in baike_item.fields:
                try:
                    baike_item[field] = eval(field)
                except NameError:
                    self.logger.debug("Field name is error" + field)
            yield baike_item
        else:
            print('连接请求失败', url)
