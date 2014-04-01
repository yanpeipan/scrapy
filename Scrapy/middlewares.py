class ProxyMiddleware(object):
  def process_request(self, request, spider):
    request.meta['proxy'] = "http://61.54.25.150:80"
    pass
