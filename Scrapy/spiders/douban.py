# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider, Spider
from scrapy.exceptions import CloseSpider
from scrapy .selector import Selector
from pymongo import MongoClient
from scrapy.http import Request
from Scrapy.items import *
import urlparse
import urllib
import json
from datetime import datetime, date, time
from scrapy.loader import ItemLoader


class DoubanSpider(CrawlSpider):
    name = 'douban'
    allowed_domins = ['http://www.douban.com', 'https://api.douban.com']
    start_urls = ['http://movie.douban.com/tag/']
    movie_tag_url = 'http://movie.douban.com/tag/'
    movie_search_url = 'https://api.douban.com/v2/movie/search'
    movei_subject_url = 'https://api.douban.com/v2/movie/subject/'
    # parse movei subject after search movie
    parse_movie_subject = False
    # rate: 40page/min
    rate = 40.0 / 60.0

    def __init__(self, *args, **kwargs):
        for k, v in enumerate(kwargs):
            setattr(self, v, kwargs[v])
        if hasattr(self, 'rate'):
            self.download_delay = 1 / getattr(self, 'rate')

    def start_requests(self):
        return [Request(self.movie_tag_url, callback=self.parseMovieTag)]

    def parseCollect(self, response):
        sel = Selector(response)
        links = sel.xpath('//div[@class="grid-view"]/div')
        links.extract()
        for index, link in enumerate(links):
            movieId = link.xpath('div[@class="info"]//a[contains(@href, "http://movie.douban.com/subject/")]').re(
                r"http://movie.douban.com/subject/(\d+)/")
        nextLink = sel.xpath(
            '//div[@class="paginator"]/span[@class="next"]/a/@href').extract()
        if len(nextLink) > 0:
            yield Request(url=nextLink.pop(), callback=self.parseCollect)

    def parseCelebrity(self, response):
        celebrity = json.loads(response.body_as_unicode())
        if len(celebrity) > 0:
            celebrityItem = CelebrityItem()
            for k, v in celebrity.iteritems():
                celebrityItem[k] = v
                yield celebrityItem

    def parseComment(self, response):
        sel = Selector(response)
        movieItem = MovieItem()
        movieItem['id'] = response.meta['id']
        commentLinks = sel.xpath(
            '//div[@id="comments"]/div[contains(@class, "comment-item")]')
        commentLinks.extract()
        comments = []
        for index, commentLink in enumerate(commentLinks):
            comment = {}
            comment['avatar'] = commentLink.xpath(
                'div[@class="avatar"]/a/img/@src').extract().pop()
            comment['uid'] = commentLink.xpath('div[@class="comment"]//span[@class="comment-info"]/a/@href').re(
                r"http://movie.douban.com/people/(.*)/").pop()
            comment['name'] = commentLink.xpath(
                'div[@class="comment"]//span[@class="comment-info"]/a/text()').extract().pop()
            comment['comment'] = commentLink.xpath(
                'div[@class="comment"]/p/text()').extract().pop()
            dateStr = commentLink.xpath(
                'div[@class="comment"]/h3/span[@class="comment-info"]/span/text()').re(r'\d+-\d+-\d+').pop()
            comment['date'] = datetime.strptime(dateStr, "%Y-%m-%d")
            comment['vote'] = int(
                commentLink.xpath('div[@class="comment"]//span[@class="comment-vote"]/span[contains(@class, "votes")]/text()').extract().pop())
            comments.append(comment)
        movieItem['comments'] = comments
        yield movieItem
        paginator = sel.xpath(
            '//div[@id="paginator"]/a[@class="next"]/@href').extract()
        parsedUrl = urlparse(response.url)
        return  # yan dd
        yield Request(url=parsedUrl.scheme + '://' + parsedUrl.netloc + parsedUrl.path + paginator.pop(), callback=self.parseComment, meta={'id': response.meta['id']})

    def parseReview(self, response):
        pass

    def parseSubject(self, response):
        sel = Selector(response)
        movieItem = MovieItem()
        movieItem['id'] = response.meta['id']
        # parse writers
        writerLinks = sel.xpath('//*[@id="info"]/span[2]/a')
        writerLinks.extract()
        writers = []
        for index, link in enumerate(writerLinks):
            writerId = link.xpath('@href').re(r"/celebrity/(\d+)/")
            if len(writerId) > 0:
                celebrity = writerId.pop()
            else:
                celebrity = None
            writer = {'id': celebrity, 'name':
                      link.xpath('text()').extract().pop()}
            writers.append(writer)
        movieItem['writers'] = writers
        # prase imdb_id
        imdbId = sel.xpath('//*[@id="info"]/a').re(
            r"http://www.imdb.com/title/(tt\d+)")
        if len(imdbId) > 0:
            movieItem['imdb_id'] = imdbId.pop()
        else:
            movieItem['imdb_id'] = None
        # parse tags
        tagLinks = sel.xpath("//div[contains(@class, 'tags-body')]/a")
        tags = []
        for i, tagLink in enumerate(tagLinks):
            tagItem = TagItem()
            tag = tagLink.xpath('text()').extract().pop()
            num = tagLink.xpath('span/text()').re(r"\((\d+)\)").pop()
            tags.append({'tag': tag, 'num': num})
        movieItem['tags'] = tags
        # yield tagItem
        # parse recommendations
        links = sel.xpath('//*[@id="recommendations"]/div/dl/dd/a')
        links.extract()
        recommendations = []
        for index, recommend in enumerate(links):
            movieId = recommend.xpath('@href').re(r"/subject/(\d+)").pop()
            movieTitle = recommend.xpath('text()').extract().pop()
            recommendations.append({'id': movieId, 'title': movieTitle})
            movieItem['recommendations'] = recommendations
            yield Request(url='https://api.douban.com/v2/movie/subject/' + movieId, callback=self.parseMovie)
        yield movieItem

    def parseMovieSubject(self, response):
        movie = json.loads(response.body_as_unicode())
        if len(movie) > 0:
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

    def parseMovieList(self, response):
        movies = json.loads(response.body_as_unicode())
        for movie in movies['subjects']:
            movieItem = MovieItem(source='douban')
            #itemLoader = ItemLoader(item=movieItem, default_output_processor=TakeFirst())
            for key in movie:
                if key in movieItem.fields:
                    movieItem[key] = movie[key]
            yield movieItem
            # parse movie subject, when self.parse_movie_subject == True
            if getattr(self, 'parse_movie_subject'):
                yield Request(url='https://api.douban.com/v2/movie/subject/' + movie['id'], callback=self.parseMovieSubject)
        if len(movies['subjects']) <= 0:
          return
        # next page
        url_parts = list(urlparse.urlparse(response.url))
        query = dict(urlparse.parse_qsl(url_parts[4]))
        if 'start' in query:
            query['start'] = (int)(query['start']) + 20
        else:
            query['start'] = 20
        url_parts[4] = urllib.urlencode(query)
        nextUrl = urlparse.urlunparse(url_parts)
        yield Request(url=nextUrl, callback=self.parseMovieList)

    def parseMovieTag(self, response):
        sel = Selector(response)
        items = sel.xpath('//table[@class="tagCol"]//td')
        for item in items:
            tag = item.xpath('a/text()').extract().pop()
            #num=item.xpath('b/text()').re(r"\d+").pop()
            yield Request(url=getattr(self, 'movie_search_url') + '?tag=' + tag, callback=self.parseMovieList)
