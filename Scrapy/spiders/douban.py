from scrapy.spider import Spider
from scrapy .selector import Selector
from Scrapy.items import TagItem,MovieItem
from pymongo import MongoClient
from scrapy.http import Request

from urlparse import urlparse,parse_qs
import json

class DoubanSpider(Spider):
  name = 'douban'
  pipeline = ['DoubanSpider']
  allowed_domins = ['http://www.douban.com', 'https://api.douban.com']
  start_urls = ['http://movie.douban.com/tag/']

  def parseMovie(self, response):
    movie = json.loads(response.body_as_unicode())
    if len(movie)>0:
      pass

  def parseList(self, response):
    movies = json.loads(response.body_as_unicode())
    if len(movies['subjects'])>0:
      for movie in movies['subjects']:
        movieItem = MovieItem()
        movieItem['rating'] = movie['rating']
        movieItem['title'] = movie['title']
        movieItem['collect_count'] = movie['collect_count']
        movieItem['original_title'] = movie['original_title']
        movieItem['year'] = movie['year']
        movieItem['alt'] = movie['alt']
        movieItem['id'] = movie['id']
        movieItem['images'] = movie['images']
        movieItem['subtype'] = movie['subtype']
        yield movieItem
      params = parse_qs(urlparse(response.url).query)
      start = (int)(params['start'].pop()) + 20
      tag = params['tag'].pop()
      yield Request(url = 'https://api.douban.com/v2/movie/search?tag=' + tag + '&start=' + str(start), callback = self.parseList)

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
      start = 0
      yield Request(url = 'https://api.douban.com/v2/movie/search?tag=' + tagItem['tag'] + '&start=' + unicode(start), callback = self.parseList)
