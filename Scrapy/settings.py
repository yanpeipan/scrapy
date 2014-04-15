# Scrapy settings for Scrapy project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'Scrapy'
USER_AGENT = 'w3m/0.5.3+cvs-1.1055'

SPIDER_MODULES = ['Scrapy.spiders']
NEWSPIDER_MODULE = 'Scrapy.spiders'

ITEM_PIPELINES = {
    'Scrapy.pipelines.ScrapyPipeline': 100,
    'Scrapy.pipelines.ProxyCrawlerPipeline':'110'
    }

DOWNLOADER_MIDDLEWARES = {
    'Scrapy.middlewares.ProxyMiddleware': 100,
    'Scrapy.middlewares.DownloadTimer': 100,
    }

SPIDER_MIDDLEWARES = {
    'Scrapy.middlewares.UrlMiddleware':1
    }

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Scrapy (+http://www.yourdomain.com)'

COOKIES_ENABLED = True

CONCURRENT_ITEMS = 1000

#LOG_ENABLED = True
#LOG_FILE = 'proxy.log'
#LOG_LEVEL = 'INFO'

DOWNLOAD_DELAY = 0.25
