from scrapy.spider import Spider
from scrapy.spider import Request
from scrapy.selector import Selector
from Scrapy.items import ProxyItem

import time

class ProxySpider(Spider):
  name = 'proxy'
  pipeline = ['ProxySpider']
  start_urls = ['http://www.baidu.com']
  urls = {'Youdaili':'http://www.youdaili.cn/Daili/http/'}

  def __init__(self, *args, **kwargs):
    pass

  def parse(self, response):
    if response.status == 200:
      self.url = response.url
      for proxy, url in self.urls.iteritems():
        yield Request(url = url, callback = self.parseYoudaili)
      return

  def parseYoudaili(self, response):
    sel = Selector(response)
    links = sel.xpath('//ul[@class="newslist_line"]/li/a/@href').extract()
    for key, link in enumerate(links):
      yield Request(url = link, callback = self.parseYoudailiDetail)

  def parseYoudailiDetail(self, response):
    sel = Selector(response)
    proxys = sel.xpath('//div[@class="cont_font"]/p').re(r"\d+.\d+.\d+.\d+:\d+")
    for proxy in proxys:
      yield Request(url=self.url + proxy, method="HEAD", meta={"proxy":'http://' + proxy, "download_timeout":10}, callback=self.parseProxy)

  def parseProxy(self, response):
    if response.status == 200:
      proxyItem = ProxyItem()
      proxyItem['ip'] = response.meta['proxy']
      proxyItem['delay'] = response.meta['endTime'] - response.meta['startTime']
      proxyItem['status'] = response.status
      yield proxyItem
