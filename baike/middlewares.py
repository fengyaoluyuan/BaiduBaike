# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import requests
import logging
from requests import ConnectionError

class ProxyMiddleware(object):

    def __init__(self, proxy_url):
        self.proxy_url = proxy_url
        self.logger = logging.getLogger(__name__)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            proxy_url=crawler.settings.get('PROXY_URL')
        )

    def get_proxy(self,):
        try:
            response = requests.get(self.proxy_url)
            if response.status_code == 200:
                print('obtain proxy success')
                ip = response.text
                return ip
            else:
                print('obtain proxy faild')
                return None
        except ConnectionError:
            print('ConnectionError')
            self.get_proxy()

    def process_request(self, request, spider):
        proxy = self.get_proxy()
        if proxy:
            request.proxy = proxy
            self.logger.debug('using proxy:' + proxy)
        else:
            self.logger.debug('no vaild proxy')

