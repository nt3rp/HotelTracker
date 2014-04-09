# -*- coding: utf-8 -*-
import random
from scrapy import log
from scrapy.exceptions import DropItem
from scrapy.mail import MailSender
import twitter
from hoteltracker.items import Hotel
import dblite

# TODO: Add logging to pipelines to make apparent that they work

# TODO: Are pipelines created for each spider?
# How can we reduce all the initialization work (if so)

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

        _, existing_item = self.availability_changed(item)

        if existing_item:
            # We can either update the date of the old item,
            # or set the id of the new item.
            item['_id'] = existing_item['_id']

        self.ds.put(item)

        return item

    def availability_changed(self, item):
        # Need to `or` with a `dict` so that we can use `existing_item`
        # even when it returns `None`

        # More info on sqlite interface here:
        # https://github.com/ownport/scrapy-dblite/blob/master/docs/dblite-api.md
        existing_item = self.ds.get({'name': item['name']}, limit=1) or {}

        was_available = bool(existing_item.get('available'))
        is_available = bool(item.get('available'))

        # An item can't change if it wasn't in the database
        if not existing_item:
            return False, item

        return (is_available is not was_available), existing_item


# We could just use the pipeline above... but we do different work,
# so keep our concerns separated.
class EmailPipeline(SqlLiteItemsPipeline):
    def process_item(self, item, spider):
        if not isinstance(item, Hotel):
            raise DropItem("Unknown item type, %s" % type(item))

        changed, existing_item = self.availability_changed(item)

        # `changed` returns true when the state goes from T->F or F->T.
        # We need to ensure that we only email if the current state is true.
        if item.get('available') and changed:
            subject = 'HotelScraper: {0} (Available)'.format(
                existing_item['name']
            )
            # TODO: Perhaps include a link to the hotel?
            # That would be useful for the twitter pipeline too...
            body = 'This hotel has now become available!'

            mailer = MailSender.from_settings(spider.settings)
            mailer.send(
                to=spider.settings['MAIL_TO'],
                subject=subject,
                body=body
            )

        return item


class TwitterPipeline(SqlLiteItemsPipeline):
    LIMIT = 140
    POST_ATTEMPTS = 3
    START = {
        "positive": [
            "",
            "Hooray! ", "Hooray; ",
            "Success! ", "Success; ",
            "Huzzah! ", "Huzzah; ",
            "Yay! ", "Yay; "
        ],
        "negative": [
            "",
            "Boo! ", "Boo; ",
            "Dang! ", "Dang; ",
            "Fail! ", "Fail; "
        ]
    }
    END = {
        "positive":  ["", "!", ".", "…", "♪", "✔"],
        "negative":  ["", "!", ".", "…", "✖"]
    }

    # Presently, unused.
    # STALE_FORMAT = '{hotel}: {start}still {rooms} available{end}'
    CHANGED_FORMAT = '{hotel}: {start}{rooms} available{end}'

    def open_spider(self, spider):
        super(TwitterPipeline, self).open_spider(spider)

        settings = spider.settings

        self.twitter = twitter.Api(
            consumer_key=settings['TWITTER_CONSUMER_KEY'],
            consumer_secret=settings['TWITTER_CONSUMER_SECRET'],
            access_token_key=settings['TWITTER_ACCESS_TOKEN_KEY'],
            access_token_secret=settings['TWITTER_ACCESS_TOKEN_SECRET']
        )

    def close_spider(self, spider):
        super(TwitterPipeline, self).close_spider(spider)

    def process_item(self, item, spider):
        # TODO: Verify that twitter API works
        changed, existing_item = self.availability_changed(item)

        available = item.get('available')

        tone = 'positive' if available else 'negative'
        rooms = 'at least one room' if available else 'no rooms'

        posted = False
        attempts = 0

        # Unlike email, we want to post a message whenever the state changes
        while changed and not posted and (attempts < self.POST_ATTEMPTS):
            message = self.CHANGED_FORMAT.format(
                hotel=item.get('name'),
                rooms=rooms,
                start=random.choice(self.START[tone]),
                end=random.choice(self.END[tone])
            )

            # Truncate to tweet limit if need be
            message = message[:self.LIMIT]

            try:
                status = self.twitter.PostUpdate(message)
            except twitter.TwitterError, e:
                attempts += 1
            else:
                posted = True

        return item