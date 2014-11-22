# -*- coding: utf-8 -*-
import scrapy


class YoukuSpider(scrapy.Spider):
    name = "youku"
    allowed_domains = ["www.youku.com"]
    show_list_url = 'http://www.youku.com/v_showlist/c0.html'
    
    def start_request(self):
	return [Request(getattr(self, 'show_list_url'))]

    def parse(self, response):
	for li in response.xpath('//*[@id="filter"]/div[1]/div/ul/li'):
		print li

