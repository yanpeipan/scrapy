# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from Scrapy.items import *

class ScrapyPipeline(object):
  def process_item(self, item, spider):
    mongo = MongoClient().scrapy
    if 'id' in item:
      if isinstance(item, MovieItem):
        if 'comments' in item:
          comments = item['comments']
          del(item['comments'])
          mongo.movies.update({'id' : item['id']}, {'$push':{'comments': {'$each':comments}}})
        mongo.movies.update({'id' : item['id']}, {'$set':dict(item)}, upsert = True)
      elif isinstance(item, CelebrityItem):
        mongo.celebritys.update({'id' : item['id']}, {'$set':dict(item)}, upsert = True)

    return item
