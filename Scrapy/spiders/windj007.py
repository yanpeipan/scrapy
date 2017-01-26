from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from Scrapy.items import ProxyItem
import re


class Windj007Spider(CrawlSpider):
    name = 'Windj007'
    start_urls = ['http://www.google.ru/search?q=%2B%94%3A8080+%2B%94%3A3128+%2B%94%3A80+filetype%3Atxt&hl=ru&source=hp&btnG=%CF%EE%E8%F1%EA+%E2+Google&gbv=1&d=1',
                  'http://www.google.ru/search?q=%2B%94%3A8080+%2B%94%3A3128+%2B%94%3A80+filetype%3Atxt&hl=ru&source=hp&btnG=%CF%EE%E8%F1%EA+%E2+Google&gbv=1&start=10',
                  'http://www.google.ru/search?q=%2B%94%3A8080+%2B%94%3A3128+%2B%94%3A80+filetype%3Atxt&hl=ru&source=hp&btnG=%CF%EE%E8%F1%EA+%E2+Google&gbv=1&start=20',
                  'http://www.google.ru/search?q=%2B%94%3A8080+%2B%94%3A3128+%2B%94%3A80+filetype%3Atxt&hl=ru&source=hp&btnG=%CF%EE%E8%F1%EA+%E2+Google&gbv=1&start=30',
                  'http://www.google.ru/search?q=%2B%94%3A8080+%2B%94%3A3128+%2B%94%3A80+filetype%3Atxt&hl=ru&source=hp&btnG=%CF%EE%E8%F1%EA+%E2+Google&gbv=1&start=40',
                  ]

    _address_re = re.compile(r'(\d{1,4}\.\d{1,4}\.\d{1,4}\.\d{1,4})[^0-9]+(\d+)')
    rules = (
        Rule(LinkExtractor(restrict_xpaths = '//h3[@class="r"]'),
             callback = 'parse_proxylist',
             follow = True
             ),
    )

    def parse_proxylist(self, response):

        if response.status >= 400:

            return

        addresses_parsed = ProxySpider._address_re.finditer(response.body)
        for row in addresses_parsed:
            res = ProxyItem()
            res['ip'] = '%s:%s' % tuple(row.groups())
            yield res
