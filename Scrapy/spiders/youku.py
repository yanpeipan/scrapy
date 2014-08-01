from scrapy.contrib.spiders import CrawlSpider
from scrapy.spider import Spider
from scrapy.exceptions import CloseSpider
from scrapy .selector import Selector
from pymongo import MongoClient
from scrapy.http import Request
from Scrapy.items import *
from urlparse import urlparse,parse_qs
import json
from datetime import datetime, date, time
from selenium import webdriver

class YoukuSpider(CrawlSpider):
  name = 'youku'
  pipelines = []
  allowed_domins = ['http://www.youku.com', 'https://api.douban.com']
  start_urls = ['http://www.youku.com/v_showlist/c0.html']

  def __init__(self, category = None, *args, **kwargs):
      if (category == 'movie'):
        pass
        #self.start_urls = ['http://www.youku.com/v_olist/c_96.html']
      pass

  def parseList(self, response):
      dr=webdriver.PhantomJS()
      dr.get(response.body)
      pageSource = dr.page_source
      dr.close()
      sel = Selector(text = pageSource, type='html')
      link = sel.xpath('//*[@id="getVideoList"]/div[1]/div[1]/div/div[3]/div[2]/a')
      nexter = 'http://www.youku.com' + sel.xpath('//*[@id="getVideoList"]/div[3]/ul/li[contains(@class, "next")]/a/@href').extract().pop()
      yield Request(url = nexter, callback = self.parseList)
      pass

  def parseFilter(self, response):
      sel = Selector(response)
      for item in sel.xpath('//div[@id="filter"]//div[contains(@class, "item")]'):
          #print item.xpath('label/text()').extract().pop()
          for li in item.xpath('.//label/text()').extract():
              print li
          pass

  def parse(self, response):
    sel = Selector(response)
    category = []
    scrapyItem = ScrapyItem()
    for item in sel.xpath('//*[@id="filter"]/div[1]/div/ul/li/a'):
        if item.xpath('@href') and item.xpath('text()'):
            scrapyItem['link'] = 'http://www.youku.com/v_showlist/c0.html' + item.xpath('@href').extract().pop()
            scrapyItem['title'] = item.xpath('text()').extract().pop()
            ##yield scrapyItem
            yield Request(url = scrapyItem['link'], callback = self.parseFilter)
