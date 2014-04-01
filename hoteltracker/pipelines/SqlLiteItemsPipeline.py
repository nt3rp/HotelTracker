from scrapy.exceptions import DropItem
from hoteltracker.items import Hotel
import dblite

# Based on the following:
# https://github.com/ownport/scrapy-dblite#how-to-use-scrapy-dblite-with-scrapy
class SqlLiteItemsPipeline(object):
    def __init__(self):
        self.ds = None

    def open_spider(self, spider):
        self.ds = dblite.open(
            Hotel,
            'sqlite://hoteltracker.sqlite:items',
            autocommit=True
        )

    def close_spider(self, spider):
        self.ds.commit()
        self.ds.close()

    def process_item(self, item, spider):
        if not isinstance(item, Hotel):
            raise DropItem("Unknown item type, %s" % type(item))

        try:
            self.ds.put(item)
        except dblite.DuplicateItem:
            raise DropItem("Duplicate item found: %s" % item)

        return item