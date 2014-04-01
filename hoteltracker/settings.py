# Scrapy settings for hoteltracker project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'hoteltracker'

SPIDER_MODULES = ['hoteltracker.spiders']
NEWSPIDER_MODULE = 'hoteltracker.spiders'

ITEM_PIPELINES = {
    'hoteltracker.pipelines.SqlLiteItemsPipeline': 800,
    'hoteltracker.pipelines.EmailPipeline': 801,
    'hoteltracker.pipelines.TwitterPipeline': 802,
}

# Mail Settings
MAIL_TO = []

# Unless you happen to be running an SMTP server, use GMail
MAIL_HOST = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_TLS = True

#MAIL_FROM = 'your_email@gmail.com'
#MAIL_USER = MAIL_FROM
#MAIL_PASS = 'your_password'

# I strongly recommend using an application specific password:
# https://support.google.com/accounts/answer/185833?hl=en

# HotelSpider Settings
DATE_FORMAT = '%Y-%m-%d'

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 ' \
             '(KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36'

# Generally, only use local_settings for mail_passwords
try:
    from local_settings import *
except ImportError:
    pass