# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
from pymongo import MongoClient
from Scrapy.items import *
from os import path
from datetime import datetime
from scrapy import log
class BasePipeline(object):
  def __init__(self):
    self.mongo = MongoClient().scrapy
  pass

class DoubanMoviePipeline(BasePipeline):
  def process_item(self, item, spider):
    self.mongo = MongoClient().scrapy

    if 'ProxySpider' in spider.pipelines:
      self.mongo.proxy.save(dict(item))
    elif 'DoubanMoviePipeline' in spider.pipelines:
      if isinstance(item, MovieItem):
        if 'comments' in item:
          comments = item['comments']
          del(item['comments'])
          self.mongo.movies.update({'id' : item['id']}, {'$push':{'comments': {'$each':comments}}})
        self.mongo.movies.update({'id' : item['id']}, {'$set':dict(item)}, upsert = True)
      elif isinstance(item, CelebrityItem):
        self.mongo.celebritys.update({'id' : item['id']}, {'$set':dict(item)}, upsert = True)
    return item
