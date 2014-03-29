# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

class ScrapyPipeline(object):
  def process_item(self, item, spider):
    mongo = MongoClient().scrapy
    #mongo.tags.insert(dict(item))
    return item
