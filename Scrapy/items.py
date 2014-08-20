# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import Join, MapCompose, TakeFirst,Identity,Compose
from datetime import datetime

class VideoItem(Item):
  source=Field()

class ScrapyItem(Item):
    title = Field()
    link = Field()
    desc = Field()

class TagItem(Item):
    tag = Field()
    num = Field()
    url = Field()

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

class MovieItem(Item):
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
