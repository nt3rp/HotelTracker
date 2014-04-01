from datetime import datetime
from scrapy.exceptions import DropItem
from scrapy.mail import MailSender
from hoteltracker.items import Hotel
import dblite

# TODO: Add logging to pipelines to make apparent that they work

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

        # More info on sqlite interface here:
        # https://github.com/ownport/scrapy-dblite/blob/master/docs/dblite-api.md
        existing_item = self.ds.get({'name': item['name']}, limit=1)

        if existing_item:
            # We can either update the date of the old item,
            # or set the id of the new item.
            item['_id'] = existing_item['_id']

        self.ds.put(item)

        return item


# We could just use the pipeline above... but we do different work,
# so keep our concerns separated.
class EmailPipeline(SqlLiteItemsPipeline):
    def process_item(self, item, spider):
        if not isinstance(item, Hotel):
            raise DropItem("Unknown item type, %s" % type(item))

        existing_item = self.ds.get({'name': item['name']}, limit=1)

        if existing_item:
            subject = 'HotelScraper: {0} (Available)'.format(
                existing_item['name']
            )
            body = 'TEST MESSAGE'

            mailer = MailSender.from_settings(spider.settings)
            mailer.send(
                to=spider.settings['MAIL_TO'],
                subject=subject,
                body=body
            )

        return item