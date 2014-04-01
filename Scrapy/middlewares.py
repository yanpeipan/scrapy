# Start your middleware class
class ProxyMiddleware(object):
  # overwrite process request
  def process_request(self, request, spider):
    print 'xxxxxxxxxxx'
    request.meta['proxy'] = "61.54.25.150"
