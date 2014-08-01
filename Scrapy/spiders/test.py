from scrapy.spider import Spider
from scrapy.spider import Request
from scrapy.selector import Selector
from Scrapy.items import ProxyItem

import time

class testSpider(Spider):
  name = 'test'
  start_urls = ['http://www.baidu.com']

  def parseBaidu(self, response):
    yield Request(url='http://www.baidu.com')
  def parse(self, response):
    yield Request(url='http://www.baidu.com')
    yield Request(url='http://www.baidu.com', callback=self.parseBaidu)


