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
