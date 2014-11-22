from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from Scrapy.items import *

class TudouSpider(CrawlSpider):
    name = 'tudou.back'
    allowed_domains = ['http://www.tudou.com']
    start_urls = ['http://www.tudou.com/']

    rules = (
        Rule(SgmlLinkExtractor(allow=r'\w+.tudou.com'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        sel = Selector(response)
        i = ScrapyItem()
        #i['domain_id'] = sel.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = sel.xpath('//div[@id="name"]').extract()
        #i['description'] = sel.xpath('//div[@id="description"]').extract()
	print i
        return i
