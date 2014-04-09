from scrapy import log, signals
from scrapy.crawler import Crawler
from scrapy.utils.project import get_project_settings
from scrapy.xlib.pydispatch import dispatcher
from twisted.internet import reactor

# TODO: Refactor such that this class is runnable and only requires data.
# Maybe use the custom command from one of the SO links as an example?

# Why is this so difficult? Why isn't a bunch of this functionality exposed
# right out of the box? I guess that's what `scrapyd` is for, but it is also
# a bit of a pain in the ass (lacks scheduling, same level of documentation).

# http://stackoverflow.com/a/17003736/165988
close_signals = 0
check_in = '2014-05-23'
check_out = '2014-05-25'
spider_list = [
    ('IHG', {
        'display_name': 'Holiday Inn - Airport East',
        'location_code': 'toronto/yyzae',
        'check_in': check_in,
        'check_out': check_out,
        'group_code': 'ANN'
    }),
    ('Radisson', {
        'location_code': ' toronto-hotel-on-m9w1j1/ontorair',
        'check_in': check_in,
        'check_out': check_out,
        'group_code': 'ANIME'
    }),
    ('InternationalPlaza', {
        'location_code': '59726',
        'check_in': check_in,
        'check_out': check_out,
        'group_code': 'ANN' # Not 100% if this is the right code...
    }),
    ('IHG', {
        'display_name': 'Crowne Plaza',
        'location_code': 'toronto/yyzca',
        'check_in': check_in,
        'check_out': check_out,
        'group_code': 'AHO'
    }),
    # ('Starwood', {
    #     'display_name': 'Sheraton',
    #     'location_code': '3508',
    #     'check_in': check_in,
    #     'check_out': check_out,
    #     # Best guess based on experimentation.
    #     # Other guesses: ANM, ANN, AHO
    #     'group_code': 'ANN'
    # }),
    ('Travelodge', {
        'location_code': 'ontario/toronto/'
                         'travelodge-hotel-toronto-airport-dixon-road',
        'check_in': check_in,
        'check_out': check_out,
        'group_code': 'CGANIM'
    })
]
spiders = len(spider_list)

# There should be no need to edit below this line.

def stop_reactor():
    global close_signals
    close_signals += 1

    if close_signals >= spiders:
        reactor.stop()

dispatcher.connect(stop_reactor, signal=signals.spider_closed)

# Original Source: http://stackoverflow.com/a/15580406/165988
def setup_crawler(name, **config):
    crawler = Crawler(settings)
    crawler.configure()

    spider = crawler.spiders.create(name, **config)
    crawler.crawl(spider)
    crawler.start()

log.start()
settings = get_project_settings()
crawler = Crawler(settings)
crawler.configure()

for item in spider_list:
    name = item[0]
    config = item[1]
    setup_crawler(name, **config)

reactor.run()