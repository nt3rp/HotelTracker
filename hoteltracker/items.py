# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class Hotel(Item):
    # `_id` is Required by `scrapy-dblite`
    #   https://github.com/ownport/scrapy-dblite/blob/master/docs/items.md
    _id = Field()
    name = Field()
    available = Field()
    last_updated = Field()
