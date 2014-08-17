#coding=utf-8
from scrapy.contrib.spiders import CrawlSpider
from scrapy.spider import Spider
from scrapy.exceptions import CloseSpider
from scrapy.selector import Selector
from scrapy.http import FormRequest
from scrapy.http import Request
from Scrapy.items import *
from urlparse import urlparse,parse_qs
import json
import os
from datetime import datetime, date, time

class YoukuSpider(CrawlSpider):

  name = 'youku'
  download_delay=0.1
  allowed_domins = ['http://www.youku.com', 'https://openapi.youku.com']
  start_urls = []

  client_id='696c961ded023528'
  """
  Apis
  """
  shows_by_category_url='https://openapi.youku.com/v2/shows/by_category.json'
  video_category_url='https://openapi.youku.com/v2/schemas/video/category.json'

  def __init__(self, category = None, *args, **kwargs):
      if category:
          self.category=category

  def start_requests(self):
      if self.category:
          data={'client_id':self.client_id, 'category':self.category}
          return [FormRequest(self.shows_by_category_url, formdata=data, callback=self.parseShowsByCategory)]
      else:
          return [Request(self.video_category_url)]

  def parseShowsByCategory(self, response):
      showItem=ShowItem()
      shows=json.loads(response.body)
      for shows in shows['shows']:
          for k in showItem.fields:
              showItem[k]=shows[k]
          yield showItem

  def parse(self, response):
      pass
