from scrapy import log, signals
from scrapy.crawler import Crawler
from scrapy.utils.project import get_project_settings
from scrapy.xlib.pydispatch import dispatcher
from twisted.internet import reactor

# TODO: Refactor such that this class is runnable and only requires data.
# Maybe use the custom command from one of the SO links as an example?

# http://stackoverflow.com/a/17003736/165988
close_signals = 0
check_in = '2014-05-02'
check_out = '2014-05-04'
spider_list = [
    ('HolidayInn', {
        'location_code': 'toronto/yyzae',
        'check_in': check_in,
        'check_out': check_out,
    })
]
spiders = len(spider_list)

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

    # Create will pass kwargs...
    # ... how can we automatically do that?
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