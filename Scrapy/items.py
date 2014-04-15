# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class ScrapyItem(Item):
  title = Field()
  link = Field()
  desc = Field()

class TagItem(Item):
  tag = Field()
  num = Field()

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
  lastTestTime = Field()
