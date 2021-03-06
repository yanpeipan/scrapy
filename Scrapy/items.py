# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, MapCompose, TakeFirst,Identity,Compose
from datetime import datetime

class VideoItem(Item):
    source=Field()
class BaidupanHotUserItem(Item):
    uk = Field()
    uname = Field()
    type = Field()
    hot_uname = Field()
    avatar_url = Field()
    intro = Field()
    user_type = Field()
    is_vip = Field()
    follow_count = Field()
    fans_count = Field()
    follow_time = Field()
    pubshare_count = Field()
    hot_uk = Field()
    album_count = Field()
class BaiduPanFansItem(Item):
    uk = Field()
    uname = Field()
    type = Field()
    fans_uname = Field()
    avatar_url = Field()
    intro = Field()
    user_type = Field()
    is_vip = Field()
    follow_count = Field()
    fans_count = Field()
    follow_time = Field()
    pubshare_count = Field()
    fans_uk = Field()
    album_count = Field()
class BaiduPanFollwItem(Item):
    uk = Field()
    uname = Field()
    type = Field()
    follow_uname = Field()
    avatar_url = Field()
    intro = Field()
    user_type = Field()
    is_vip = Field()
    follow_count = Field()
    fans_count = Field()
    follow_time = Field()
    pubshare_count = Field()
    follow_uk = Field()
    album_count = Field()
class BaiduPanShareItem(Item):
    cover_thumb = Field()
    operation = Field()
    album_id = Field()
    feed_type = Field()
    category = Field()
    public = Field()
    shareid = Field()
    data_id = Field()
    title = Field()
    third = Field()
    clienttype = Field()
    filecount = Field()
    uk = Field()
    username = Field()
    feed_time = Field()
    desc = Field()
    avatar_url = Field()
    category_1_cnt = Field()
    category_2_cnt = Field()
    category_3_cnt = Field()
    category_4_cnt = Field()
    category_5_cnt = Field()
    category_6_cnt = Field()
    category_7_cnt = Field()
    category_8_cnt = Field()
    category_9_cnt = Field()
    dir_cnt = Field()
    filelist = Field()
    source_uid = Field()
    source_id = Field()
    shorturl = Field()
    vCnt = Field()
    dCnt = Field()
    tCnt = Field()
    like_status = Field()
    like_count = Field()
    comment_count = Field()

class CelebrityItem(Item):
    mobile_url = Field()
    aka_en = Field()
    name = Field()
    works = Field()
    gender = Field()
    avatars = Field()
    id = Field()
    aka = Field()
    name_en = Field()
    born_place = Field()
    alt = Field()

class Person(Item):
    id = Field()
    name = Field()
    icon = Field()
    collect = Field()
    wish = Field()

class MovieItem(VideoItem):
    rating = Field()
    title = Field()
    collect_count = Field()
    original_title = Field()
    subtype = Field()
    year = Field()
    images = Field()
    alt = Field()
    id = Field()
    reviews_count = Field()
    wish_count = Field()
    douban_site = Field()
    mobile_url= Field()
    title= Field()
    do_count= Field()
    seasons_count= Field()
    schedule_url= Field()
    episodes_count= Field()
    countries= Field()
    genres= Field()
    collect_count= Field()
    casts= Field()
    current_season= Field()
    original_title= Field()
    summary= Field()
    subtype= Field()
    directors= Field()
    comments_count= Field()
    ratings_count= Field()
    aka= Field()
    writers = Field()
    imdb_id = Field()
    tags = Field()
    recommendations = Field()
    comments = Field()
    reviews = Field()

class ProxyItem(Item):
    ip = Field()
    delay = Field()
    type = Field()
    anonymity = Field()
    status = Field()
    time = Field()

class streamtypes(Item):
    hd2=Field()
    flv=Field()
    hd=Field()
    hd3gp=Field()
    hd3=Field()

class ShowItem(VideoItem):
    id=Field()
    name=Field()
    link=Field()
    play_link=Field()
    last_play_link=Field()
    poster=Field()
    thumbnail=Field()
    streamtypes=Field()
    hasvideotype=Field()
    completed=Field()
    episode_count=Field(serializer=int)
    episode_updated=Field()
    category=Field()
    view_count=Field(serializer=int)
    source=Field()
    paid=Field()
    published=Field()
    released=Field()
    comment_count=Field(serializer=int)
    favorite_count=Field(serializer=int)
    lastupdate=Field()
    dma=Field()
    type=Field()
    dct=Field()
    algInfo=Field()
    related=Field()

class ShowLoader(ItemLoader):

    default_output_processor=TakeFirst()

    streamtypes_out=Identity()
    hasvideotype_out=Identity()
    #published_out=Compose(lambda s:datetime.strptime(s[0], '%Y-%m-%d'))

    favorite_count_in=MapCompose(int)
    episode_count_in=MapCompose(int)
    view_count_in=MapCompose(int)
    comment_count_in=MapCompose(int)

class ShowVideoItem(Item):
    show_id=Field()
    id=Field()
    title=Field()
    link=Field()
    thumbnail=Field()
    duration=Field()
    category=Field()
    view_count=Field()
    favorite_count=Field()
    comment_count=Field()
    up_count=Field()
    down_count=Field()
    stage=Field()
    seq=Field()
    published=Field()
    operation_limit=Field()
    streamtypes=Field()
    state=Field()
    rc_title=Field()

class UncomplatedItem(Item):
  id=Field()
