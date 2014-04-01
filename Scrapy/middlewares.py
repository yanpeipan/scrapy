class ProxyMiddleware(object):
  def process_request(self, request, spider):
    #request.meta['proxy'] = "http://118.186.69.62:80"
    request = request.replace(url = "%s&apikey=00d8ef49d1c2b3bb028acddd75481b31" % request.url)
    request.meta['proxy'] = 'http://24.143.198.188:80'

class UrlMiddleware(object):
  def _process_start_requests(self, requests, spider):
    print requests
    for request in requests:
      pass
      #request.replace(url = "%s&apikey=00d8ef49d1c2b3bb028acddd75481b31" % request.url)
    print requests
    return requests
