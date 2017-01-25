# -*- coding: utf-8 -*-

from scrapy.contrib.spiders import CrawlSpider
from scrapy.spider import Spider
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


class PanBaiduSpider(CrawlSpider):
  name = 'douban'
  uks = ['286353630']
  allowed_domins = ['https://pan.baidu.com']
  #缺少专辑列表
  URL_SHARE = 'http://yun.baidu.com/pcloud/feed/getsharelist?auth_type=1&start={start}&limit=20&query_uk={uk}&urlid={id}' #获得分享列表
  """
  {"feed_type":"share","category":6,"public":"1","shareid":"1541924625","data_id":"2418757107690953697","title":"\u5723\u8bde\u58c1\u7eb8\u5927\u6d3e\u9001","third":0,"clienttype":0,"filecount":1,"uk":1798788396,"username":"SONYcity03","feed_time":1418986714000,"desc":"","avatar_url":"http:\/\/himg.bdimg.com\/sys\/portrait\/item\/1b6bf333.jpg","dir_cnt":1,"filelist":[{"server_filename":"\u5723\u8bde\u58c1\u7eb8\u5927\u6d3e\u9001","category":6,"isdir":1,"size":1024,"fs_id":870907642649299,"path":"%2F%E5%9C%A3%E8%AF%9E%E5%A3%81%E7%BA%B8%E5%A4%A7%E6%B4%BE%E9%80%81","md5":"0","sign":"1221d7d56438970225926ad552423ff6a5d3dd33","time_stamp":1439542024}],"source_uid":"871590683","source_id":"1541924625","shorturl":"1dDndV6T","vCnt":34296,"dCnt":7527,"tCnt":5056,"like_status":0,"like_count":60,"comment_count":19},
  public:公开分享
  title:文件名称
  uk:用户编号
  """
  URL_FOLLOW = 'http://yun.baidu.com/pcloud/friend/getfollowlist?query_uk={uk}&limit=20&start={start}&urlid={id}' #获得订阅列表
  """
  {"type":-1,"follow_uname":"\u597d\u55e8\u597d\u55e8\u554a","avatar_url":"http:\/\/himg.bdimg.com\/sys\/portrait\/item\/979b832f.jpg","intro":"\u9700\u8981\u597d\u8d44\u6599\u52a0994798392","user_type":0,"is_vip":0,"follow_count":2,"fans_count":2276,"follow_time":1415614418,"pubshare_count":36,"follow_uk":2603342172,"album_count":0},
  follow_uname:订阅名称
  fans_count：粉丝数
  """
  URL_FANS = 'http://yun.baidu.com/pcloud/friend/getfanslist?query_uk={uk}&limit=20&start={start}&urlid={id}' # 获取关注列表
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
    for uk in uks:
      requests.append(Request(self.URL_SHARE.format(uk=uk), callback=self.parseMovieTag))
    return requests
  """
  解析分享列表
  """
  def parseShareList(self):
      pass
  """
  解析粉丝
  """
  def parseFans(self):
      pass
  """
  解析关注
  """
  def parseFollow(self):
      pass
