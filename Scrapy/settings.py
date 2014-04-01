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
    'Scrapy.pipelines.ScrapyPipeline': 300,
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
    'Scrapy.middlewares.ProxyMiddleware': 100,
    'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': 90,
    }

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Scrapy (+http://www.yourdomain.com)'

COOKIES_ENABLED = False
