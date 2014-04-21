from scrapy.spider import Spider
from scrapy.spider import Request
from scrapy.selector import Selector
from Scrapy.items import ProxyItem
from selenium import webdriver
from scrapy.selector import HtmlXPathSelector

import time

class ProxySpider(Spider):
  name = 'proxy'
  pipelines = ['ProxySpider']
  middlewares = ['Selenium']
  start_urls = ['http://www.baidu.com']
  urls = {
      #'Youdaili':'http://www.youdaili.cn/Daili/http/',
      #'Hidemyass':'https://hidemyass.com/proxy-list/',
      'Cnproxy':'http://www.cnproxy.com/proxy1.html'
      }

  def __init__(self, *args, **kwargs):
    pass
  def parse(self, response):
    if response.status == 200:
      self.url = response.url
      for proxy, url in self.urls.iteritems():
        yield Request(url = url, callback = getattr(self, 'parse' + proxy))

  def parseCnproxyDetail(self, response):
    pass

  def parseCnproxy(self, response):
    dr=webdriver.PhantomJS()
    dr.get(response.url)
    pageSource = dr.page_source
    dr.close()
    sel = Selector(text = pageSource, type='html')
    trs = sel.xpath('//*[@id="proxylisttb"]/table[3]//tr[1]/following-sibling::tr')
    for key, tr in enumerate(trs):
      result = tr.re(r'(\d+(?:\.\d+){3})(?:.*)(:\d+)')
      if len(result) == 2:
        proxy = result[0] + result[1]
        yield Request(url=self.url + '?' + proxy, method="HEAD", meta={"proxy":'http://' + proxy, "download_timeout":10}, callback=self.parseProxy)

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

