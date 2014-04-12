from scrapy.spider import Spider
from scrapy.spider import Request
from scrapy.selector import Selector
from scrapy.conf import settings

import scrapy.settings
import socket

class ProxySpider(Spider):
  name = 'proxy'
  pipeline = ['ProxySpider']
  start_urls = ['http://www.youdaili.cn/Daili/http/']

  def __init__(self, *args, **kwargs):
    pass

  def parse(self, response):
    sel = Selector(response)
    links = sel.xpath('//ul[@class="newslist_line"]/li/a/@href').extract()
    for key, link in enumerate(links):
      yield Request(url = link, callback = self.parseYoudaili)
      return

  def parseYoudaili(self, response):
    settings.overrides['DOWNLOAD_TIMEOUT'] = 5
    settings.overrides['CONCURRENT_REQUESTS'] = 32
    sel = Selector(response)
    proxys = sel.xpath('//div[@class="cont_font"]/p').re(r"\d+.\d+.\d+.\d+:\d+")
    for proxy in proxys:
      yield Request(url='http://www.baidu.com?' + proxy, meta={"proxy":'http://' + proxy}, callback=self.parseProxy)

  def parseProxy(self, response):
    print response.status
