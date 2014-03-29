from scrapy.spider import Spider
from scrapy .selector import Selector
from Scrapy.items import TagItem
from pymongo import MongoClient
from scrapy.http import Request
import json

class DoubanSpider(Spider):
  name = 'douban'
  pipeline = ['DoubanSpider']
  allowed_domins = ["http://www.douban.com", "https://api.douban.com"]
  start_urls = [
      "http://movie.douban.com/tag/"
      ]
  def parseList(self, response):
    movie = json.loads(response.body_as_unicode())
    if len(movie['subjects'])>0:
      url = ''
      yield Request(url = '', callback = self.parseList)

  def parse(self, response):
    mongo = MongoClient().scrapy
    sel = Selector(response)
    items = sel.xpath('//table[@class="tagCol"]//td')
    tags = []
    for item in items:
      tagItem = TagItem()
      tagItem['tag'] = item.xpath('a/text()').extract().pop()
      tagItem['num'] = item.xpath('b/text()').re(r"\d+").pop()
      tags.append(TagItem)
      self.collection = "tags"
      yield tagItem
      yield Request(url = "https://api.douban.com/v2/movie/search?tag=" + tagItem["tag"], meta = {"start":0}, callback = self.parseList)
