from scrapy.contrib.spiders import CrawlSpider
from scrapy.spider import Spider
from scrapy .selector import Selector
from pymongo import MongoClient
from scrapy.http import Request
from Scrapy.items import *

from urlparse import urlparse,parse_qs
import json

class DoubanSpider(CrawlSpider):
  name = 'douban'
  pipeline = ['DoubanSpider']
  allowed_domins = ['http://www.douban.com', 'https://api.douban.com']
  start_urls = ['http://movie.douban.com/tag/']

  def parseCelebrity(self, response):
    celebrity = json.loads(response.body_as_unicode())
    if len(celebrity)>0:
      celebrityItem = CelebrityItem()
      for k,v in celebrity.iteritems():
        celebrityItem[k] = v
        yield celebrityItem

  def parseSubject(self, response):
    sel = Selector(response)
    movieItem = MovieItem()
    movieItem['id'] = response.meta['id']
    #parse writers
    writerLinks = sel.xpath('//*[@id="info"]/span[2]/a')
    writerLinks.extract()
    writers = []
    for index, link in enumerate(writerLinks):
      writer = {'id':link.xpath('@href').re(r"/celebrity/(\d+)/"), 'name':link.xpath('text()').extract()}
      writers.append(writer)
    movieItem['writers'] = writers
    movieItem['imdb_id'] = sel.xpath('//*[@id="info"]/a').re(r"http://www.imdb.com/title/(tt\d+)").pop()
    tags = sel.xpath('//*[@id="content"]/div/div[2]/div[3]/div/a').extract()
    recommendations = sel.xpath('//*[@id="recommendations"]/div/dl/dd/a').re(r"/subject/(\d+)")

  def parseMovie(self, response):
    movie = json.loads(response.body_as_unicode())
    if len(movie)>0:
      movieItem = MovieItem()
      for k, v in movie.iteritems():
        movieItem[k] = v
      yield movieItem
      for celebrity in (movie['casts'] + movie['directors']):
        if id in celebrity:
          yield Request(url = 'https://api.douban.com/v2/movie/celebrity/' + celebrity['id'], callback = self.parseCelebrity)
      yield Request(url = 'http://movie.douban.com/subject/' + movie['id'], callback = self.parseSubject, meta = {'id':movie['id']})

  def parseList(self, response):
    print response.url
    movies = json.loads(response.body_as_unicode())
    if len(movies['subjects'])>0:
      for movie in movies['subjects']:
        yield Request(url = 'https://api.douban.com/v2/movie/subject/' + movie['id'], callback = self.parseMovie)
      params = parse_qs(urlparse(response.url).query)
      start = (int)(params['start'].pop()) + 20 #also can be translated by request.meta
      tag = params['tag'].pop()
      #yield Request(url = 'https://api.douban.com/v2/movie/search?tag=' + tag + '&start=' + str(start), callback = self.parseList)

  def parse(self, response):
    sel = Selector(response)
    items = sel.xpath('//table[@class="tagCol"]//td')
    for item in items:
      tagItem = TagItem()
      tagItem['tag'] = item.xpath('a/text()').extract().pop()
      tagItem['num'] = item.xpath('b/text()').re(r"\d+").pop()
      yield tagItem
      yield Request(url = 'https://api.douban.com/v2/movie/search?tag=' + tagItem['tag'] + '&start=0', callback = self.parseList)
      return#yan wait for dd
