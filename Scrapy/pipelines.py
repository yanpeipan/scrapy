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

    if 'DoubanMovie' in spider.pipelines:
      if isinstance(item, MovieItem):
        if 'comments' in item:
          comments = item['comments']
          del(item['comments'])
          self.mongo.movies.update({'id' : item['id']}, {'$push':{'comments': {'$each':comments}}})
        self.mongo.movies.update({'id' : item['id']}, {'$set':dict(item)}, upsert = True)
      elif isinstance(item, CelebrityItem):
        self.mongo.celebritys.update({'id' : item['id']}, {'$set':dict(item)}, upsert = True)
    return item

class ProxyCrawlerPipeline(object):
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings['PROXY_CHECK_TIMEOUT'] or 10.0,
                   crawler.settings['PROXY_CHECK_THREADS'] or 50,
                   crawler.settings['PROXY_RESULTS_FILE'] or None)

    def __init__(self, timeout = 1.0, check_threads = 50, result_file = None):
        if not result_file:
            #res_dir = path.join(path.dirname(__file__), 'results')
            res_dir = path.dirname(__file__)
            self._res_filename = path.join(res_dir,  datetime.today().strftime('proxies_%Y_%m_%d_%H_%M.lst'))
            if path.exists(self._res_filename):
                os.remove(self._res_filename)
                #log.msg("Remove previously created %s" % self._res_filename, log.WARNING)
        else:
            self._res_filename = result_file

        #self._out_file = open(self._res_filename, 'a')
        #log.msg("Will write extracted addresses to %s" % self._res_filename, log.INFO)

        self._timeout = timeout
        log.msg("Connection timeout is %s" % self._timeout, log.INFO)

    def process_item(self, item, spider):
      if 'ProxyCrawlerSpider' in spider.pipelines:
        pass
        #log.msg("Gonna write %s" % item['address'], log.DEBUG)

    def close_spider(self, spider):
      pass
      #self._out_file.flush()
      #self._out_file.close()
