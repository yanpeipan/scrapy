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
    'Scrapy.pipelines.DoubanMoviePipeline': 100,
    #'Scrapy.pipelines.ProxyCrawlerPipeline':'110'
    }

DOWNLOADER_MIDDLEWARES = {
    'Scrapy.middlewares.ProxyMiddleware': 100,
    'Scrapy.middlewares.DownloadTimer': 100,
    }

#SPIDER_MIDDLEWARES = {
#    'Scrapy.middlewares.UrlMiddleware':1
#    }


COOKIES_ENABLED = False

CONCURRENT_ITEMS = 1000

#LOG_ENABLED = True
#LOG_FILE = 'ScrapyCrawl.log'
#LOG_LEVEL = 'INFO'

DOWNLOAD_DELAY = 0.25

STATS_CLASS = 'Scrapy.graphite.RedisGraphiteStatsCollector'
