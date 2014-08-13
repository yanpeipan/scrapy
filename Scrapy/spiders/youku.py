#coding=utf-8
from scrapy.contrib.spiders import CrawlSpider
from scrapy.spider import Spider
from scrapy.exceptions import CloseSpider
from scrapy.selector import Selector
from scrapy.http import FormRequest
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
  allowed_domins = ['http://www.youku.com', 'https://api.douban.com', 'https://openapi.youku.com']
  start_urls = ['http://www.youku.com/v_showlist/c0.html']

  def __init__(self, category = None, *args, **kwargs):
      if category:
          self.category=category

  def start_requests(self):
      return [FormRequest('https://openapi.youku.com/v2/shows/by_category.json', formdata={'client_id':'696c961ded023528', 'category':self.category}, callback=self.parse)]

  def parseCategory(self, response):
      pass

  def parse(self, response):
      showItem=ShowItem()
      shows=json.loads(response.body)
      for show in shows['shows']:
          showItem['id']=show['id']
          yield showItem
