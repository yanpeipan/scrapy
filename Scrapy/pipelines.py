# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import pymongo
from Scrapy.items import *
from os import path
from datetime import datetime
from scrapy import log
from scrapy.contrib.exporter import BaseItemExporter


class BasePipeline(object):

  def __init__(self):
    pass


class MongoPipeline(BasePipeline):

  def __init__(self):
    self.mongo = pymongo.MongoClient()

  def process_item(self, item, spider):

    if isinstance(item, ShowItem):
      exporter=BaseItemExporter()
      #print type(exporter.serialize_field(item.fields['favorite_count'], 'favorite_count', '333'))
      if 'id' in item:
        self.mongo.scrapy.videos.update({'id':item['id']}, {'$set':dict(item)}, upsert=True)

    if 'ProxyItem' == item.__class__.__name__:
      self.mongo.Scrapy.proxy.save(dict(item))

    if 'MovieItem' == item.__class__.__name__:
      if isinstance(item, MovieItem):
        if 'comments' in item:
          comments = item['comments']
          del(item['comments'])
          self.mongo.Scrapy.movies.update({'id' : item['id']}, {'$push':{'comments': {'$each':comments}}})
        self.mongo.Scrapy.movies.update({'id' : item['id']}, {'$set':dict(item)}, upsert = True)
      elif isinstance(item, CelebrityItem):
        self.mongo.Scrapy.celebritys.update({'id' : item['id']}, {'$set':dict(item)}, upsert = True)
    return item
