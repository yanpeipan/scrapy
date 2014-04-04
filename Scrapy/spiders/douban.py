from scrapy.contrib.spiders import CrawlSpider
from scrapy.spider import Spider
from scrapy.exceptions import CloseSpider
from scrapy .selector import Selector
from pymongo import MongoClient
from scrapy.http import Request
from Scrapy.items import *
from urlparse import urlparse,parse_qs
import json
from datetime import datetime, date, time

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

  def parseComment(self, response):
    sel = Selector(response)
    movieItem = MovieItem()
    movieItem['id'] = response.meta['id']
    commentLinks = sel.xpath('//div[@id="comments"]/div[contains(@class, "comment-item")]')
    commentLinks.extract()
    comments = []
    for index, commentLink in enumerate(commentLinks):
      comment = {}
      comment['avatar'] = commentLink.xpath('div[@class="avatar"]/a/img/@src').extract().pop()
      comment['uid'] = commentLink.xpath('div[@class="comment"]//span[@class="comment-info"]/a/@href').re(r"http://movie.douban.com/people/(.*)/").pop()
      comment['name'] = commentLink.xpath('div[@class="comment"]//span[@class="comment-info"]/a/text()').extract().pop()
      comment['comment'] = commentLink.xpath('div[@class="comment"]/p/text()').extract().pop()
      dateStr = commentLink.xpath('div[@class="comment"]/h3/span[@class="comment-info"]/span/text()').re(r'\d+-\d+-\d+').pop()
      comment['date']= datetime.strptime(dateStr, "%Y-%m-%d")
      comment['vote'] = int(commentLink.xpath('div[@class="comment"]//span[@class="comment-vote"]/span[contains(@class, "votes")]/text()').extract().pop())
      comments.append(comment)
    movieItem['comments'] = comments
    yield movieItem
    paginator = sel.xpath('//div[@id="paginator"]/a[@class="next"]/@href').extract()
    parsedUrl = urlparse(response.url)
    return#yan dd
    yield Request(url = parsedUrl.scheme + '://' + parsedUrl.netloc + parsedUrl.path + paginator.pop(), callback = self.parseComment, meta = {'id':response.meta['id']})

  def parseReview(self, response):
    pass

  def parseSubject(self, response):
    sel = Selector(response)
    movieItem = MovieItem()
    movieItem['id'] = response.meta['id']
    #parse writers
    writerLinks = sel.xpath('//*[@id="info"]/span[2]/a')
    writerLinks.extract()
    writers = []
    for index, link in enumerate(writerLinks):
      writerId = link.xpath('@href').re(r"/celebrity/(\d+)/")
      if len(writerId)>0:
        celebrity = writerId.pop()
      else:
        celebrity = None
      writer = {'id':celebrity, 'name':link.xpath('text()').extract().pop()}
      writers.append(writer)
    movieItem['writers'] = writers
    #prase imdb_id
    movieItem['imdb_id'] = sel.xpath('//*[@id="info"]/a').re(r"http://www.imdb.com/title/(tt\d+)").pop()
    #parse tags
    tagLinks = sel.xpath("//div[contains(@class, 'tags-body')]/a")
    tags = []
    for i, tagLink in enumerate(tagLinks):
      tagItem = TagItem()
      tag = tagLink.xpath('text()').extract().pop()
      num = tagLink.xpath('span/text()').re(r"\((\d+)\)").pop()
      tags.append({'tag':tag, 'num':num})
    movieItem['tags'] = tags
    #yield tagItem
    #parse recommendations
    links = sel.xpath('//*[@id="recommendations"]/div/dl/dd/a')
    links.extract()
    recommendations = []
    for index, recommend in enumerate(links):
      movieId = recommend.xpath('@href').re(r"/subject/(\d+)").pop()
      movieTitle = recommend.xpath('text()').extract().pop()
      recommendations.append({'id':movieId, 'title':movieTitle})
      movieItem['recommendations'] = recommendations
      yield Request(url = 'https://api.douban.com/v2/movie/subject/' + movieId, callback = self.parseMovie)
    yield movieItem

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
      yield Request(url = 'http://movie.douban.com/subject/' + movie['id'] + '/comments', callback = self.parseComment, meta = {'id':movie['id']})
      yield Request(url = 'http://movie.douban.com/subject/' + movie['id'] + '/reviews', callback = self.parseReview, meta = {'id':movie['id']})

  def parseList(self, response):
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
