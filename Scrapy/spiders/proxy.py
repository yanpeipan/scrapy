from scrapy.spider import Spider
from scrapy.spider import Request
from scrapy.selector import Selector

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
    sel = Selector(response)
    proxys = sel.xpath('//div[@class="cont_font"]/p').re(r"\d+.\d+.\d+.\d+:\d+")
    for proxy in proxys:
      proxy = 'http://' + proxy
      yield Request(url = proxy, callback = self.parseProxy)

  def CheckProxy(ip,port):
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.settimeout(1)#设置链连接时时间
    try:
      sk.connect((ip,port))
      print 'OK'
    except Exception:
      print 'NO'

  def parseProxy(self, response):
    print response.headers
