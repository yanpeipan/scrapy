#coding=utf-8
from scrapy.contrib.spiders import CrawlSpider
from scrapy.spider import Spider
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Join
from scrapy.exceptions import CloseSpider
from scrapy.selector import Selector
from scrapy.http import FormRequest
from scrapy.http import Request
from Scrapy.items import *
from urlparse import urlparse,parse_qs
import json
import pymongo
from datetime import datetime, date, time

class YoukuSpider(CrawlSpider):
    name = 'youku'
    #download_delay=3600/1000
    allowed_domins = ['http://www.youku.com', 'https://openapi.youku.com']
    start_urls = []

    """
    config of youku
    """
    client_id='696c961ded023528'
    max_matches=1500
    parse_videos_after_show=False
    #1000/hour
    #@link http://open.youku.com/docs/newbieguide.html#id4
    rate=float(1000)/3600
    #@link http://open.youku.com/docs/api_searches.html#schemas-unit
    schemas_unit=['美国', '大陆', '香港', '日本', '韩国', '台湾', '俄罗斯', '英国', '意大利',
'朝鲜', '法国', '泰国', '加拿大', '新加坡', '印度', '伊朗', '澳大利亚', '南斯拉夫',
'西班牙', '新西兰', '菲律宾', '丹麦', '捷克', '瑞典', '匈牙利', '澳门', '阿富汗',
'阿根廷', '阿联酋', '埃及', '爱尔兰', '奥地利', '巴拉圭', '巴勒斯坦', '巴西', '德国',
'保加利亚', '比利时', '冰岛', '波黑', '波兰', '芬兰', '哥伦比亚', '格鲁吉亚', '智利',
'古巴', '荷兰', '柬埔寨', '克罗地亚', '黎巴嫩', '利比亚', '卢森堡', '罗马尼亚', '越南',
'马来西亚', '马其顿', '蒙古', '秘鲁', '墨西哥', '南非', '尼日利亚', '挪威', '葡萄牙',
'瑞士', '突尼斯', '土耳其', '乌拉圭', '希腊', '以色列', '印度尼西亚', '其他']

    """
    Apis
    """
    shows_by_category_url='https://openapi.youku.com/v2/shows/by_category.json'
    show_category_url='https://openapi.youku.com/v2/schemas/show/category.json'
    shows_show_url='https://openapi.youku.com/v2/shows/show.json'
    shows_videos_url='https://openapi.youku.com/v2/shows/videos.json'

    def __init__(self, category = None, *args, **kwargs):
        self.mongo=pymongo.MongoClient()
        if hasattr(self, 'rate'):
            self.download_delay=1/getattr(self, 'rate')
        if category:
            self.category=unicode(category, 'utf-8')
        for k,v in enumerate(kwargs):
            if not hasattr(self, v):
                setattr(self, v, kwargs[v])

    def start_requests(self):
        if hasattr(self, 'type') and getattr(self, 'type') == 'uncompleted videos':
            requests=[]
            for show in self.mongo.scrapy.videos.find({'completed':0}):
                requests.append(self.queryShowsVideos({'show_id':show['id']}))
            return requests
        elif hasattr(self, 'show_id') and hasattr(self, 'videos'):
            #update videos of show which id is `show_id`
            return [self.queryShowsVideos({'show_id':getattr(self, 'show_id')})]
        else:
            #update all
            return [Request(self.show_category_url, callback=self.parseCategory)]

    def parseCategory(self, response):
        categories=json.loads(response.body)
        if 'categories' in categories:
            for category in categories['categories']:
                category_label=category['label']
                if hasattr(self, 'category') and self.category != category_label:
                    continue
                if 'genre' in category:
                    data={'client_id':self.client_id, 'category':category_label, 'page':'1', 'count':'100'}
                    if hasattr(self, 'year'):
                        data['release_year']=getattr(self, 'year')
                    if hasattr(self, 'area'):
                        data['area']=getattr(self, 'area')
                    if hasattr(self, 'orderby'):
                        data['orderby']=getattr(self, 'orderby')
                    for genre in category['genre']:
                        data['genre']=genre['label']
                        yield self.queryShowsByCategory(data)
                    else:
                        yield self.queryShowsByCategory(data)
                else:
                    raise

    def parseShowsByCategory(self, response):
        shows=json.loads(response.body)
        if 'total' in shows:
            shows_total=int(shows['total'])
            if shows_total == 0:
                return
            # add subclass(area, release_year),if total of shows greater than max_matches
            elif shows_total > self.max_matches:
                data=response.meta['formdata']
                if 'area' not in response.meta['formdata']:
                    for area in self.schemas_unit:
                        data['area']=area
                        yield self.queryShowsByCategory(data)
                elif 'release_year' not in response.meta['formdata']:
                    years=range(2008, datetime.now().year+1)
                    years.append(9999)
                    for year in years:
                        data['release_year']=str(year)
                        yield self.queryShowsByCategory(data)
                else:
                    raise
                return
        if 'shows' in shows:
            for show in shows['shows']:
                if 'id' in show:
                    pass
                    #yield self.queryShowsVideos({'client_id':self.client_id, 'show_id':str(show['id'])})
                else:
                    continue
                showItem=ShowItem(source='youku')
                itemLoader = ShowLoader(item=showItem)
                for k in show:
                    if k in showItem.fields:
                        showItem[k]=show[k]
                        itemLoader.add_value(k, show[k])
                yield itemLoader.load_item()
        else:
            raise
        # add subclass(area, release_year),if total of shows greater than max_matches
        for show in shows['shows']:
            #parse videos of show
            if 'id' in show and getattr(self, 'parse_videos_after_show'):
                yield self.queryShowsVideos({'client_id':self.client_id, 'show_id':str(show['id'])})
            showItem=ShowItem(source='youku')
            itemLoader = ShowLoader(item=showItem)
            for k in show:
                if k in showItem.fields:
                    showItem[k]=show[k]
                    itemLoader.add_value(k, show[k])
            yield itemLoader.load_item()
        #next page
        if "formdata" in response.meta and all(key in response.meta['formdata'] for key in ['page', 'count', 'category']):
            page=int(response.meta['formdata']['page'])
            next_page=page+1
            count=int(response.meta['formdata']['count'])
        if next_page*count < self.max_matches and page*count < shows_total:
            data=response.meta['formdata']
            data['page']=str(next_page)
            yield self.queryShowsByCategory(data)

    def queryShowsByCategory(self, formdata):
        #check necessary keys
        if all(key in formdata for key in ['client_id', 'category']): return FormRequest(self.shows_by_category_url, formdata=formdata, callback=self.parseShowsByCategory, meta={'formdata':formdata}) 

    def queryShowsVideos(self, formdata):
        #check necessary keys
        if all(key in formdata for key in ['show_id']):
            formdata['count']=str(formdata['count']) if 'count' in formdata else '100'
            formdata['page']=str(formdata['page']) if 'page' in formdata else '1'
            formdata['client_id']=str(formdata['client_id']) if 'client_id' in formdata else self.client_id
            #formdata['show_videotype']=str(formdata['show_videotype']) if 'show_videotype' in formdata else '正片,预告片,花絮,MV,资讯,首映式'
            formdata['orderby']=str(formdata['orderby']) if 'orderby' in formdata else 'videoseq-asc'
            return FormRequest(self.shows_videos_url, formdata=formdata, callback=self.parseShowsVideos, meta={'formdata':formdata})
        else:
            pass


    def parseShowsVideos(self, response):
        if 'formdata' not in response.meta or 'show_id' not in response.meta['formdata']:
            return
        #init variables
        formdata=response.meta['formdata']
        videos=json.loads(response.body)
        count=int(formdata['count']) if 'count' in formdata else 20
        page=int(formdata['page']) if 'page' in formdata else 1
        total=int(videos['total']) if 'total' in videos else False
        show_id=response.meta['formdata']['show_id']
        #videos
        if 'videos' in videos:
            for video in videos['videos']:
                showVideoItem=ShowVideoItem({'show_id':show_id})
                for k in video:
                    if k in showVideoItem.fields:
                        showVideoItem[k]=video[k]
                yield showVideoItem
        #next page
        if total > page*count:
            formdata['page']=str(page+1)
            yield self.queryShowsVideos(formdata)

    def parseShow(self, response):
        pass
