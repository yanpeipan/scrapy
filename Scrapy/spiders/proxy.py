from scrapy.spider import Spider
from scrapy.spider import Request
from scrapy.selector import Selector
from Scrapy.items import ProxyItem

import time

class ProxySpider(Spider):
  name = 'proxy'
  pipelines = ['ProxySpider']
  start_urls = ['http://www.baidu.com']
  urls = {
      'Youdaili':'http://www.youdaili.cn/Daili/http/',
      'Hidemyass':'https://hidemyass.com/proxy-list/',
      'Cnproxy':'http://www.cnproxy.com/proxy1.html'
      }

  def __init__(self, *args, **kwargs):
    pass

  def parse(self, response):
    if response.status == 200:
      self.url = response.url
      for proxy, url in self.urls.iteritems():
        yield Request(url = url, callback = getattr(self, 'parse' + proxy))
      return

  def parseCnproxy(self, response):
    sel = Selector(response)
    trs = sel.xpath('//*[@id="proxylisttb"]/table[3]/tbody/tr')
    print trs.extract()
    return

  def parseHidemyass(self, response):
    return

  def parseYoudaili(self, response):
    return
    sel = Selector(response)
    links = sel.xpath('//ul[@class="newslist_line"]/li/a/@href').extract()
    for key, link in enumerate(links):
      yield Request(url = link, callback = self.parseYoudailiDetail)
      return

  def parseYoudailiDetail(self, response):
    sel = Selector(response)
    proxys = sel.xpath('//div[@class="cont_font"]/p').re(r"\d+.\d+.\d+.\d+:\d+")
    for proxy in proxys:
      yield Request(url=self.url + '?' + proxy, method="HEAD", meta={"proxy":'http://' + proxy, "download_timeout":10}, callback=self.parseProxy)

  def parseProxy(self, response):
    proxyItem = ProxyItem()
    proxyItem['ip'] = response.meta['proxy']
    proxyItem['delay'] = response.meta['endTime'] - response.meta['startTime']
    proxyItem['status'] = response.status
    proxyItem['time'] = time.time()
    yield proxyItem

