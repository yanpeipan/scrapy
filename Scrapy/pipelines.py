#coding=utf-8
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html import os
import pymongo
from Scrapy.items import *
from os import path
from datetime import datetime
from scrapy import log
from scrapy.contrib.exporter import BaseItemExporter

class BasePipeline(object):

  def __init__(self):
    pass


"""
Serializer
"""
class SerializerPipeline(BasePipeline):

  def process_item(self, item, spider):
    itemExporter=BaseItemExporter()
    for k,v in enumerate(item):
      item[v]=itemExporter.serialize_field(item.fields[v], v, item[v])


"""
MongoDB
"""
class MongoPipeline(BasePipeline):

  def __init__(self):
    self.mongo = pymongo.MongoClient()

  def process_item(self, item, spider):

    if isinstance(item, ShowItem):
      if 'id' in item:
        self.mongo.scrapy.videos.update({'id':item['id']}, {'$set':dict(item)}, upsert=True)
    #upsert youku videos
    if isinstance(item, ShowVideoItem) and 'id' in item and 'show_id' in item:
        self.mongo.scrapy.videos.update({'id':item['show_id']}, {'$setOnInsert':{'videos':dict(item)}, '$set': {'videos':dict(item)}}, False, True)
        #self.mongo.scrapy.videos.update({'id':item['show_id']}, {'$addToSet':{'videos':dict(item)}}, True, True)
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
