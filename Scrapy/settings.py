# Scrapy settings for Scrapy project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'Scrapy'

SPIDER_MODULES = ['Scrapy.spiders']
NEWSPIDER_MODULE = 'Scrapy.spiders'

ITEM_PIPELINES = {
    'Scrapy.pipelines.MongoPipeline': 100,
    }

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
    'Scrapy.middlewares.ProxyMiddleware': 99,
    'scrapy_proxies.RandomProxy': 100,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    'Scrapy.middlewares.BaiduyunMiddleware': 560,
    }

SPIDER_MIDDLEWARES = {
   }
CONCURRENT_ITEMS = 100
CONCURRENT_REQUESTS = 16
CONCURRENT_REQUESTS_PER_DOMAIN = 8

REACTOR_THREADPOOL_MAXSIZE = 10

COOKIES_ENABLED = False

CONCURRENT_ITEMS = 1000

LOG_ENABLED = True
#LOG_FILE = 'ScrapyCrawl.log'
#LOG_LEVEL = 'INFO'

DOWNLOAD_DELAY = 0.25

GRAPHITE_HOST = '127.0.0.1'
GRAPHITE_PORT = 2003
#STATS_CLASS = 'Scrapy.graphite.RedisGraphiteStatsCollector'
DEPTH_LIMIT = 0
DEPTH_PRIORITY = 1
DEPTH_STATS = True

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_DEBUG = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 300

RETRY_ENABLED = True
RETRY_TIMES = 3

PROXY_LIST = '/tmp/ip-good.txt'
