#coding=utf-8
from scrapy.contrib.spiders import CrawlSpider
from scrapy.spider import Spider
from scrapy.exceptions import CloseSpider
from scrapy .selector import Selector
from pymongo import MongoClient
from scrapy.http import Request
from Scrapy.items import *
from urlparse import urlparse,parse_qs
import json
import os
import tempfile
from datetime import datetime, date, time
from selenium import webdriver

class YoukuSpider(CrawlSpider):
  name = 'youku'
  pipelines = []
  allowed_domins = ['http://www.youku.com', 'https://api.douban.com']
  start_urls = ['http://www.youku.com/v_showlist/c0.html']

  def __init__(self, category = None, *args, **kwargs):
      if (category == 'movie'):
        self.start_urls = ['http://www.youku.com/v_olist/c_96.html']
      pass

  def parse(self, response):
      sel = Selector(response)
      if sel.xpath('//div[@name="total_videonum"]'):
          total = sel.xpath('//div[@name="total_videonum"]/text()').extract().pop()
      #youku限制
      if int(total) == 1200:
          pass
      tags = {}

      for item in sel.xpath('//div[@id="filter"]//div[contains(@class, "item")]'):
          tag = {}
          print tag
          if item.xpath('.//label/text()'):
              tag['tag'] = item.xpath('.//label/text()').extract().pop()
              #print tag
          for index,link in enumerate(item.xpath('.//li/a')):
              tag['items'][index] = {'name':link.xpath('text()').extract().pop(),'link':link.xpath('@href').extract().pop()}
      print tags
      print tag

  def parseF(self, response):
    sel = Selector(response)
    category = []
    scrapyItem = ScrapyItem()
    for item in sel.xpath('//*[@id="filter"]/div[1]/div/ul/li/a'):
        if item.xpath('@href') and item.xpath('text()'):
            scrapyItem['link'] = 'http://www.youku.com/v_showlist/c0.html' + item.xpath('@href').extract().pop()
            scrapyItem['title'] = item.xpath('text()').extract().pop()
            yield Request(url = scrapyItem['link'], callback = self.parseFilter)
