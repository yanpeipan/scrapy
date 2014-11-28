from urlparse import urlparse,parse_qs
from pymongo import MongoClient
import time
import random
from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware
from selenium import webdriver

class ProxyMiddleware(object):
  def __init__(self):
    mongo = MongoClient().scrapy
    self.proxys = list(mongo.proxy.find({'status':200}))

  def process_request(self, request, spider):
    print request.meta
    if spider.__class__.__name__ == 'DoubanSpider':
      url = urlparse(request.url)
      params = parse_qs(url.query)
      if url.scheme == 'https':
        if len(url.query) == 0:
          request = request.replace(url = "%s?apikey=0d58236c3758bc2928086a44a60a347b" % request.url)
        elif 'apikey' not in parse_qs(url.query):
          request = request.replace(url = "%s&apikey=0d58236c3758bc2928086a44a60a347b" % request.url)
        else:
          return
        return request
      elif url.scheme == 'http':
	pass
      elif 'Selenium' in getattr(spider, 'middlewares', []):
        pass
      #browser = webdriver.Firefox()
      #browser.get(request.url)

  def process_response(self, request, response, spider):
    if response.status != 200:
      pass
    return response
  def process_exception(self, request, exception, spider):
    pass

class UrlMiddleware(object):
  def process_request(self, request, spider):
    pass
  def _process_start_requests(self, requests, spider):
    for request in requests:
      pass
    return requests

class DownloadTimer(object):
  def process_request(self, request, spider):
    request.meta['startTime'] = time.time()
  def process_response(self, request, response, spider):
    request.meta['endTime'] = time.time()
    return response



class RotateUserAgentMiddleware(UserAgentMiddleware):
  user_agent_list = [\
      'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.43 Safari/537.31',\
      'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17',\
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17',\
      \
      'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.2; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)',\
      'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',\
      'Mozilla/5.0 (Windows; U; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)',\
      \
      'Mozilla/6.0 (Windows NT 6.2; WOW64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1',\
      'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:15.0) Gecko/20100101 Firefox/15.0.1',\
      'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:15.0) Gecko/20120910144328 Firefox/15.0.2',\
      \
      'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',\
      'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9a3pre) Gecko/20070330',\
      'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.13; ) Gecko/20101203',\
      \
      'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14',\
      'Opera/9.80 (X11; Linux x86_64; U; fr) Presto/2.9.168 Version/11.50',\
      'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; de) Presto/2.9.168 Version/11.52',\
      \
      'Mozilla/5.0 (Windows; U; Win 9x 4.90; SG; rv:1.9.2.4) Gecko/20101104 Netscape/9.1.0285',\
      'Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:1.8.1.7pre) Gecko/20070815 Firefox/2.0.0.6 Navigator/9.0b3',\
      'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',\
      ]

  def process_request(self, request, spider):
    if hasattr(spider, 'user_agent'):
      agent = spider.user_agent
    elif self.user_agent:
      agent = self.user_agent
    else:
      agent = random.choice(getattr(self, 'user_agent_list'))
    if agent:
      request.headers.setdefault('User-Agent', agent)
