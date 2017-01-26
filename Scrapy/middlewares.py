from urlparse import urlparse,parse_qs
from pymongo import MongoClient
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from selenium import webdriver
import time
import random
import json

class ProxyMiddleware(object):
  def __init__(self):
    mongo = MongoClient().scrapy
    self.proxys = list(mongo.proxy.find({'status':200}))

  def process_request(self, request, spider):
    if spider.__class__.__name__ == 'DoubanSpider':
      url = urlparse(request.url)
      params = parse_qs(url.query)
      if url.scheme == 'https':
        if len(url.query) == 0:
          request = request.replace(url = "%s?apikey=0d58236c3758bc2928086a44a60a347b" % request.url)
        elif 'apikey' not in parse_qs(url.query):
          request = request.replace(url = "%s&apikey=0d58236c3758bc2928086a44a60a347b" % request.url)
        else:
          return
        return request
      elif url.scheme == 'http':
	pass
      elif 'Selenium' in getattr(spider, 'middlewares', []):
        pass
      #browser = webdriver.Firefox()
      #browser.get(request.url)

  def process_response(self, request, response, spider):
    if response.status != 200:
      pass
    return response
  def process_exception(self, request, exception, spider):
    pass

class BaiduyunMiddleware(object):
  def process_response(self, request, response, spider):
      if spider.__class__.__name__ == 'BaidupanSpider':
          list = json.loads(response.body_as_unicode())
          if list['errno'] != 0:
              return response.replace(status=500)
      return response
