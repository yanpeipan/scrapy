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
  def getListFromApi(self, response):
    movie = json.loads(response.body_as_unicode())
    print response.url
    if len(movie['subjects']) > 0:
      pass

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
      yield tagItem
      yield Request(url = "https://api.douban.com/v2/movie/search?tag=" + tagItem["tag"], callback = self.getListFromApi)
