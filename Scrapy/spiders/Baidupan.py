# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from Scrapy.items import *
import json

class BaidupanSpider(CrawlSpider):
  name = 'baidupan'
  uks = []
  allowed_domins = ['https://pan.baidu.com']
  URL_HOT = 'https://pan.baidu.com/pcloud/friend/gethotuserlist?start={start}&limit=24'
  """
  {"errno":0,"request_id":3296180617,"hotuser_list":[{"type":-1,"hot_uname":"\u6700\u7ec8***4\u4e91\u76d8","avatar_url":"https:\/\/ss0.bdstatic.com\/7Ls0a8Sm1A5BphGlnYG\/sys\/portrait\/item\/50424c4f.jpg","intro":"\u767e\u5ea6\u300a\u6700\u7ec8\u5e7b\u60f314\u300b\u4e91\u5e73\u53f0\u30028\u670825\u65e5\u5f00\u653e\u6027\u6d4b\u8bd5\u5f00\u542f\uff0c\u656c\u8bf7\u671f\u5f85\u3002","follow_count":0,"fans_count":1278735,"user_type":4,"is_vip":0,"pubshare_count":2,"hot_uk":1112219283,"album_count":3},{"type":-1,"hot_uname":"\u8273*\u90ed\u9759","avatar_url":"https:\/\/ss0.bdstatic.com\/7Ls0a8Sm1A5BphGlnYG\/sys\/portrait\/item\/7a567d4d.jpg","intro":"\u90ed\u9759\u4e0e15\u4e2a\u57ce\u5e02\u7684\u8273\u9047","follow_count":0,"fans_count":1370108,"user_type":4,"is_vip":0,"pubshare_count":0,"hot_uk":1447638178,"album_count":0}]}
  """
  URL_INFO = 'https://pan.baidu.com/pcloud/user/getinfo?&query_uk={uk}'
  """
  {"errno":0,"request_id":456845460,"user_info":{"avatar_url":"https:\/\/ss0.bdstatic.com\/7Ls0a8Sm1A5BphGlnYG\/sys\/portrait\/item\/decad705.jpg","fans_count":1,"follow_count":1,"intro":"","uname":"\u65adVS\u5f26","uk":3389100040,"album_count":0,"pubshare_count":0,"tui_user_count":0,"c2c_user_sell_count":0,"c2c_user_buy_count":0,"c2c_user_product_count":0,"pair_follow_type":-1}}
  uname:昵称
  """
  #缺少专辑列表
  URL_SHARE_LIMIT = 100
  URL_SHARE = 'https://pan.baidu.com/pcloud/feed/getsharelist?&auth_type=1&start={start}&limit=100&query_uk={uk}' #获得分享列表
  """
  {"feed_type":"share","category":6,"public":"1","shareid":"1541924625","data_id":"2418757107690953697","title":"\u5723\u8bde\u58c1\u7eb8\u5927\u6d3e\u9001","third":0,"clienttype":0,"filecount":1,"uk":1798788396,"username":"SONYcity03","feed_time":1418986714000,"desc":"","avatar_url":"http:\/\/himg.bdimg.com\/sys\/portrait\/item\/1b6bf333.jpg","dir_cnt":1,"filelist":[{"server_filename":"\u5723\u8bde\u58c1\u7eb8\u5927\u6d3e\u9001","category":6,"isdir":1,"size":1024,"fs_id":870907642649299,"path":"%2F%E5%9C%A3%E8%AF%9E%E5%A3%81%E7%BA%B8%E5%A4%A7%E6%B4%BE%E9%80%81","md5":"0","sign":"1221d7d56438970225926ad552423ff6a5d3dd33","time_stamp":1439542024}],"source_uid":"871590683","source_id":"1541924625","shorturl":"1dDndV6T","vCnt":34296,"dCnt":7527,"tCnt":5056,"like_status":0,"like_count":60,"comment_count":19},
  public:公开分享
  title:文件名称
  uk:用户编号
  """
  URL_FOLLOW_LIMIT = 24
  URL_FOLLOW = 'https://pan.baidu.com/pcloud/friend/getfollowlist?query_uk={uk}&limit={limit}&start={start}' #获得订阅列表
  """
  {"type":-1,"follow_uname":"\u597d\u55e8\u597d\u55e8\u554a","avatar_url":"http:\/\/himg.bdimg.com\/sys\/portrait\/item\/979b832f.jpg","intro":"\u9700\u8981\u597d\u8d44\u6599\u52a0994798392","user_type":0,"is_vip":0,"follow_count":2,"fans_count":2276,"follow_time":1415614418,"pubshare_count":36,"follow_uk":2603342172,"album_count":0},
  follow_uname:订阅名称
  fans_count：粉丝数
  """
  URL_FANS_LIMIT = 24
  URL_FANS = 'https://pan.baidu.com/pcloud/friend/getfanslist?query_uk={uk}&limit={limit}&start={start}' # 获取关注列表
  """
  {"type":-1,"fans_uname":"\u62e8\u52a8\u795e\u7684\u5fc3\u7eea","avatar_url":"http:\/\/himg.bdimg.com\/sys\/portrait\/item\/d5119a2b.jpg","intro":"","user_type":0,"is_vip":0,"follow_count":8,"fans_count":39,"follow_time":1439541512,"pubshare_count":15,"fans_uk":288332613,"album_count":0}
  avatar_url：头像
  fans_uname：用户名
  """
  # rate: 20page/min
  rate = 20.0 / 60.0
  parse_fans = False
  parse_share_list = True
  parse_share_priority = -100

  def __init__(self, *args, **kwargs):
      for k, v in enumerate(kwargs):
          setattr(self, v, kwargs[v])
      if hasattr(self, 'rate'):
          self.download_delay = 1 / getattr(self, 'rate')

  def start_requests(self):
    requests = []
    start = 0
    hotUserRequest = Request(
        url=self.URL_HOT.format(start=start),
        callback=self.parseHotUserList,
        meta={'start': start}
    )
    requests.append(hotUserRequest)
    for _,uk in enumerate(self.uks):
        shareListRequest = Request(
            url=self.URL_SHARE.format(uk=uk, start=start, limit=self.URL_SHARE_LIMIT),
            callback=self.parseShareList,
            headers={'Referer':'https://pan.baidu.com/share/home'},
            meta={'uk': uk, 'start': start, 'limit': self.URL_SHARE_LIMIT},
            priority=self.parse_share_priority
        )
        fansRequest = Request(
            url=self.URL_FANS.format(uk=uk, start=start, limit=self.URL_FANS_LIMIT),
            callback=self.parseFans,
            meta={'uk': uk, 'start': start, 'limit': self.URL_FANS_LIMIT}
        )
        followRequest = Request(
            url=self.URL_FOLLOW.format(uk=uk, start=start, limit=self.URL_FOLLOW_LIMIT),
            callback=self.parseFollow,
            meta={'uk': uk, 'start': start, 'limit': self.URL_FOLLOW_LIMIT}
        )
        #requests.append(shareListRequest)
        # requests.append(fansRequest)
        #requests.append(followRequest)

    return requests
  """
  解析热门用户列表
  """
  def parseHotUserList(self, response):
      list = json.loads(response.body_as_unicode())
      if list['errno'] == 0:
          for _, record in enumerate(list['hotuser_list']):
              yield BaidupanHotUserItem(record)
              uk = record['hot_uk']
              if (record['pubshare_count'] > 0 or record['album_count'] > 0) and self.parse_share_list:
                  yield Request(
                      url=self.URL_SHARE.format(uk=uk, start=0, limit=self.URL_SHARE_LIMIT),
                      callback=self.parseShareList,
                      headers={'Referer':'https://pan.baidu.com/share/home'},
                      meta={'uk': uk, 'start': 0, 'limit': self.URL_SHARE_LIMIT},
                      priority=self.parse_share_priority
                  )
              if record['fans_count'] > 0 and self.parse_fans:
                  yield Request(
                      url=self.URL_FANS.format(uk=uk, start=0, limit=self.URL_FANS_LIMIT),
                      callback=self.parseFans,
                      meta={'uk': uk, 'start': 0, 'limit': self.URL_FANS_LIMIT}
                  )
              if record['follow_count'] > 0:
                  yield Request(
                      url=self.URL_FOLLOW.format(uk=uk, start=0, limit=self.URL_FOLLOW_LIMIT),
                      callback=self.parseFollow,
                      meta={'uk': uk, 'start': 0, 'limit': self.URL_FOLLOW_LIMIT}
                  )
          if len(list) > 0:
              start = response.meta['start'] + 24
              yield Request(
                url=self.URL_HOT.format(start=start),
                callback=self.parseHotUserList,
                meta={'start': start}
              )
  """
  解析分享列表
  """
  def parseShareList(self, response):
      list = json.loads(response.body_as_unicode())
      if list['errno'] == 0:
          for _,record in enumerate(list['records']):
              yield BaiduPanShareItem(record)
          # next page
          start = response.meta['start']
          totalCount = (int)(list['total_count'])
          if (start + 1) < totalCount and self.parse_share_list:
              uk = response.meta['uk']
              start = start + self.URL_SHARE_LIMIT
              limit = self.URL_SHARE_LIMIT
              yield Request(
                  url=self.URL_SHARE.format(uk=uk, start=start, limit=limit),
                  callback=self.parseShareList,
                  meta={'uk': uk, 'start': start, 'limit': limit},
                  priority=self.parse_share_priority
              )

  """
  解析粉丝
  """
  def parseFans(self, response):
      list = json.loads(response.body_as_unicode())
      print(list)
      if list['errno'] == 0:
          start = response.meta['start']
          for _,record in enumerate(list['fans_list']):
              # 解析粉丝的关注，粉丝，分享列表（start从0开始
              yield BaiduPanFansItem(record)
              uk = record['fans_uk']
              if (record['pubshare_count'] > 0 or record['album_count'] > 0) and self.parse_share_list :
                  yield Request(
                      url=self.URL_SHARE.format(uk=uk, start=0, limit=self.URL_SHARE_LIMIT),
                      callback=self.parseShareList,
                      headers={'Referer':'https://pan.baidu.com/share/home'},
                      meta={'uk': uk, 'start': 0, 'limit': self.URL_SHARE_LIMIT},
                      priority=self.parse_share_priority
                  )
              if record['fans_count'] > 0 and self.parse_fans:
                  yield Request(
                      url=self.URL_FANS.format(uk=uk, start=0, limit=self.URL_FANS_LIMIT),
                      callback=self.parseFans,
                      meta={'uk': uk, 'start': 0, 'limit': self.URL_FANS_LIMIT}
                  )
              if record['follow_count'] > 0:
                  yield Request(
                      url=self.URL_FOLLOW.format(uk=uk, start=0, limit=self.URL_FOLLOW_LIMIT),
                      callback=self.parseFollow,
                      meta={'uk': uk, 'start': 0, 'limit': self.URL_FOLLOW_LIMIT}
                  )

          # next page
          start = response.meta['start']
          totalCount = (int)(list['total_count'])
          if (start + 1) < totalCount and self.parse_fans:
              print('next')
              uk = response.meta['uk']
              start = start + self.URL_FANS_LIMIT
              yield Request(
                  url=self.URL_FANS.format(uk=uk, start=start, limit=self.URL_FANS_LIMIT),
                  callback=self.parseFans,
                  meta={'uk': uk, 'start': start, 'limit': self.URL_FANS_LIMIT}
              )
  """
  解析关注
  """
  def parseFollow(self, response):
      list = json.loads(response.body_as_unicode())
      start = response.meta['start']
      if list['errno'] == 0:
          for _,record in enumerate(list['follow_list']):
              yield BaiduPanFollwItem(record)
              # 请求分享列表
              if (record['pubshare_count'] > 0 or record['album_count'] > 0) and self.parse_share_list :
                  yield Request(
                      url=self.URL_SHARE.format(uk=record['follow_uk'], start=0, limit=self.URL_SHARE_LIMIT),
                      callback=self.parseShareList,
                      headers={'Referer':'https://pan.baidu.com/share/home'},
                      meta={'uk': record['follow_uk'], 'start': 0, 'limit': self.URL_SHARE_LIMIT},
                      priority=self.parse_share_priority
                  )
              if record['fans_count'] > 0 and self.parse_fans:
                  yield Request(
                      url=self.URL_FANS.format(uk=record['follow_uk'], start=0, limit=self.URL_FANS_LIMIT),
                      callback=self.parseFans,
                      meta={'uk': record['follow_uk'], 'start': 0, 'limit': self.URL_FANS_LIMIT}
                  )
              if record['follow_count'] > 0:
                  yield Request(
                      url=self.URL_FOLLOW.format(uk=record['follow_uk'], start=0, limit=self.URL_FOLLOW_LIMIT),
                      callback=self.parseFollow,
                      meta={'uk': record['follow_uk'], 'start': 0, 'limit': self.URL_FOLLOW_LIMIT}
                  )
          # next page
          start = response.meta['start']
          totalCount = (int)(list['total_count'])
          if (start + 1) < totalCount and self.parse_fans:
              uk = response.meta['uk']
              start = start + self.URL_FOLLOW_LIMIT
              yield Request(
                  url=self.URL_FOLLOW.format(uk=uk, start=start, limit=self.URL_FOLLOW_LIMIT),
                  callback=self.parseFollow,
                  meta={'uk': uk, 'start': start, 'limit': self.URL_FOLLOW_LIMIT}
              )
