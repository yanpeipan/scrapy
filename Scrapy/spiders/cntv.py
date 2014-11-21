# -*- coding: utf-8 -*-
import scrapy


class CntvSpider(scrapy.Spider):
	name = "cntv"
	allowed_domains = ["http://tv.cntv.cn"]
	videoset_search='http://tv.cntv.cn/videoset/search'
	#init
	def __init__(self, *args, **kwargs):
		pass
	#start request
	def start_requests(self):
		return [scrapy.http.Request(url=getattr(self, 'videoset_search'))]
	#parse  code
	def parse(self, response):
		print response.xpath('//dd[@code]')
		pass
