# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider
from scrapy.exceptions import CloseSpider
from scrapy .selector import Selector
from pymongo import MongoClient
from scrapy.http import Request
from Scrapy.items import *
import urlparse
import urllib
import json
from datetime import datetime, date, time
from scrapy.contrib.loader import ItemLoader


class BaidupanSpider(CrawlSpider):
  name = 'baidupan'
  uks = ['286353630', '3842858568']
  allowed_domins = ['https://pan.baidu.com']
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
  # parse movei subject after search movie
  parse_movie_subject = False
  # rate: 40page/min
  rate = 40.0 / 60.0

  def __init__(self, *args, **kwargs):
      for k, v in enumerate(kwargs):
          setattr(self, v, kwargs[v])
      if hasattr(self, 'rate'):
          self.download_delay = 1 / getattr(self, 'rate')

  def start_requests(self):
    requests = []
    start = 0
    for _,uk in enumerate(self.uks):
        shareListRequest = Request(
            url=self.URL_SHARE.format(uk=uk, start=start, limit=self.URL_SHARE_LIMIT),
            callback=self.parseShareList,
            headers={'Referer':'https://pan.baidu.com/share/home'},
            meta={'uk': uk, 'start': start, 'limit': self.URL_SHARE_LIMIT},
            priority=100
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
        requests.append(shareListRequest)
        requests.append(fansRequest)
        requests.append(followRequest)

    return requests
  """
  请求分享列表
  """
  def requestShareList(self, uk, start, limit):
      yield Request(
          url=self.URL_FANS.format(uk=uk, start=start, limit=limit),
          callback=self.parseShareList,
          meta={'uk': uk, 'start': start, 'limit': limit}
      )
  """
  请求粉丝列表
  """
  def requestFans(self, uk, start, limit):
      yield Request(
          url=self.URL_FANS.format(uk=uk, start=start, limit=limit),
          callback=self.parseFans,
          meta={'uk': uk, 'start': start, 'limit': limit}
      )
  """
  请求关注列表
  """
  def requestFollow(self, uk, start, limit):
      yield Request(
          url=self.URL_FOLLOW.format(uk=uk, start=start, limit=limit),
          callback=self.parseFollow,
          meta={'uk': uk, 'start': start, 'limit': limit}
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
          totalCount = list['total_count']
          if start * self.URL_SHARE_LIMIT < totalCount:
              uk = response.meta['uk']
              start = start + self.URL_SHARE_LIMIT
              limit = self.URL_SHARE_LIMIT
              yield Request(
                  url=self.URL_SHARE.format(uk=uk, start=start, limit=limit),
                  callback=self.parseShareList,
                  meta={'uk': uk, 'start': start, 'limit': limit},
                  priority=100
              )

  """
  解析粉丝
  """
  def parseFans(self, response):
      list = json.loads(response.body_as_unicode())
      if list['errno'] == 0:
          start = response.meta['start']
          for _,record in enumerate(list['fans_list']):
              # 解析粉丝的关注，粉丝，分享列表（start从0开始
              uk = record['fans_uk']
              yield Request(
                  url=self.URL_SHARE.format(uk=uk, start=0, limit=self.URL_SHARE_LIMIT),
                  callback=self.parseShareList,
                  headers={'Referer':'https://pan.baidu.com/share/home'},
                  meta={'uk': record['fans_uk'], 'start': 0, 'limit': self.URL_SHARE_LIMIT},
                  priority=100
              )
              yield Request(
                  url=self.URL_FANS.format(uk=uk, start=0, limit=self.URL_FANS_LIMIT),
                  callback=self.parseFans,
                  meta={'uk': uk, 'start': 0, 'limit': self.URL_FANS_LIMIT}
              )
              yield Request(
                  url=self.URL_FOLLOW.format(uk=uk, start=0, limit=self.URL_FOLLOW_LIMIT),
                  callback=self.parseFollow,
                  meta={'uk': uk, 'start': 0, 'limit': self.URL_FOLLOW_LIMIT}
              )

          # next page
          start = response.meta['start']
          totalCount = list['total_count']
          if start * self.URL_FANS_LIMIT < totalCount:
              uk = response.meta['uk']
              start = start + self.URL_FANS_LIMIT
              self.requestFans(uk, start, self.URL_FANS_LIMIT)
  """
  解析关注
  """
  def parseFollow(self, response):
      list = json.loads(response.body_as_unicode())
      start = response.meta['start']
      if list['errno'] == 0:
          for _,record in enumerate(list['follow_list']):
            # 请求分享列表
            yield Request(
                url=self.URL_SHARE.format(uk=record['follow_uk'], start=0, limit=self.URL_SHARE_LIMIT),
                callback=self.parseShareList,
                headers={'Referer':'https://pan.baidu.com/share/home'},
                meta={'uk': record['follow_uk'], 'start': 0, 'limit': self.URL_SHARE_LIMIT},
                priority=100
            )
            yield Request(
                url=self.URL_FANS.format(uk=record['follow_uk'], start=0, limit=self.URL_FANS_LIMIT),
                callback=self.parseFans,
                meta={'uk': record['follow_uk'], 'start': 0, 'limit': self.URL_FANS_LIMIT}
            )
            yield Request(
                url=self.URL_FOLLOW.format(uk=record['follow_uk'], start=0, limit=self.URL_FOLLOW_LIMIT),
                callback=self.parseFollow,
                meta={'uk': record['follow_uk'], 'start': 0, 'limit': self.URL_FOLLOW_LIMIT}
            )

          # next page
          start = response.meta['start']
          totalCount = list['total_count']
          if start * self.URL_FOLLOW < totalCount:
              uk = response.meta['uk']
              start = start + self.URL_FOLLOW
              self.requestFans(uk, start, self.URL_FOLLOW)
      pass
