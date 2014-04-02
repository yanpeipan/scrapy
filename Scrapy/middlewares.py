from urlparse import urlparse,parse_qs

class ProxyMiddleware(object):
  def process_request(self, request, spider):
    url = urlparse(request.url)
    params = parse_qs(url.query)
    if url.scheme == 'https':
      if len(url.query) == 0:
        request = request.replace(url = "%s?apikey=00d8ef49d1c2b3bb028acddd75481b31" % request.url)
      elif 'apikey' in parse_qs(url.query):
        return
      request = request.replace(url = "%s&apikey=00d8ef49d1c2b3bb028acddd75481b31" % request.url)
      return request
    elif url.scheme == 'http':
      #request.meta['proxy'] = 'http://24.143.198.188:80'
      pass

  def process_response(self, request, response, spider):
    return response

class UrlMiddleware(object):
  def process_request(self, request, spider):
    pass
  def _process_start_requests(self, requests, spider):
    print requests
    for request in requests:
      pass
      #request.replace(url = "%s&apikey=00d8ef49d1c2b3bb028acddd75481b31" % request.url)
    print requests
    return requests
