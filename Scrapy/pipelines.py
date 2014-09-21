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
    #upsert youku show
    if isinstance(item, ShowItem) and getattr(item, 'id'):
        result=self.mongo.scrapy.videos.update({'id':item['id']}, {'$set':dict(item)}, upsert=True)
    #upsert youku videos when 'ShowVideoItem' == item.__class__.__name__
    if isinstance(item, ShowVideoItem) and 'id' in item and 'show_id' in item:
      result = self.mongo.scrapy.videos.update({'id':item['show_id'], 'videos.id':item['id']}, {'$set':{'videos.$':dict(item)}}, False, True)
      if result['updatedExisting'] == False:
        self.mongo.scrapy.videos.update({'id':item['show_id']}, {'$addToSet':{'videos':dict(item)}}, False, True)
    if 'ProxyItem' == item.__class__.__name__:
      self.mongo.scrapy.proxy.save(dict(item))
    #upsert douban movie
    if isinstance(item, MovieItem):
      if 'comments' in item:
        self.mongo.scrapy.videos.update({'id' : item['id']}, {'$push':{'comments': {'$each': item['comments']}}})
        del(item['comments'])
      self.mongo.scrapy.videos.update({'id' : item['id']}, {'$set':dict(item)}, upsert = True)
    if isinstance(item, CelebrityItem):
      self.mongo.scrapy.celebritys.update({'id' : item['id']}, {'$set':dict(item)}, upsert = True)
    return item
