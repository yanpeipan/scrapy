#coding=utf-8
from scrapy.contrib.spiders import CrawlSpider
from scrapy.spider import Spider
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Join
from scrapy.exceptions import CloseSpider
from scrapy.selector import Selector
from scrapy.http import FormRequest
from scrapy.http import Request
from Scrapy.items import *
from urlparse import urlparse,parse_qs
import json
import pymongo
from datetime import datetime, date, time

class TudouSpider(CrawlSpider):

    name = 'tudou'
    allowed_domins = ['http://www.tudou.com']
    list_url = 'http://www.tudou.com/list/index.html'

    rate=float(1000)/3600

    def __init__(self, category = None, *args, **kwargs):
        if hasattr(self, 'rate'):
            self.download_delay=1/getattr(self, 'rate')
        if category:
            self.category=unicode(category, 'utf-8')

    def start_requests(self):
	return [Request(getattr(self, 'list_url'), callback=self.parseList)]

    def parseList(self, response):
	channels=response.xpath('//*[@id="secMenu"]/ul/li')	
	for channel in channels:
	    id=channel.xpath('@data-id').extract()
	    url=channel.xpath('.//a/@href').extract()
	    name=channel.xpath('.//a/text()').extract()
	
