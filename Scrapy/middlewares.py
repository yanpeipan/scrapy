from urlparse import urlparse,parse_qs
import time

class ProxyMiddleware(object):
  def process_request(self, request, spider):
    if 'DoubanSpider' in getattr(spider, 'pipelines', []):
      url = urlparse(request.url)
      params = parse_qs(url.query)
      if url.scheme == 'https':
        if len(url.query) == 0:
          request = request.replace(url = "%s?apikey=00d8ef49d1c2b3bb028acddd75481b31" % request.url)
        elif 'apikey' not in parse_qs(url.query):
          request = request.replace(url = "%s&apikey=00d8ef49d1c2b3bb028acddd75481b31" % request.url)
        else:
          return
      elif url.scheme == 'http':
        request.meta['proxy'] = 'http://139.210.98.86:8080'

  def process_response(self, request, response, spider):
    return response

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
