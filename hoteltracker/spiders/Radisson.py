from time import strftime, strptime
from datetime import datetime
from scrapy.http import FormRequest
from scrapy.selector import Selector
from scrapy.spider import Spider
from scrapy.utils.response import open_in_browser
from urlparse import urlparse
from hoteltracker.items import Hotel


class RadissonSpider(Spider):
    name = "Radisson"
    allowed_domains = ["radisson.com"]
    url_template = 'http://www.radisson.com/{0}'
    time_format = '%m/%d/%Y'

    def __init__(self, location_code=None, check_in=None, check_out=None):
        if not location_code:
            location_code = 'toronto-hotel-on-m9w1j1/ontorair'

        # TODO: Seriously check for missing check in / out.
        if not check_in:
            check_in = '2014-05-03'

        if not check_out:
            check_out = '2014-05-05'

        self.start_urls = [self.url_template.format(location_code)]

        # Expect dates in ISO 8601, i.e. Oct 9 1988 -> 1988-10-09
        # TODO: Get default time format from project
        self.check_in = strftime(self.time_format, strptime(check_in, '%Y-%m-%d'))
        self.check_out = strftime(self.time_format, strptime(check_out, '%Y-%m-%d'))


    def parse(self, response):
        sel = Selector(response)
        urls = sel.css('[name=rateSearchForm]::attr(action)')

        if not urls:
            # log something
            pass

        hostname = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(response.url))
        path = '{0}{1}'.format(hostname, urls[0].extract())

        return [FormRequest(
            url=path,
            formdata={ # TODO: Which of these is critical
                'rateSearchForm.crossBrandSearch': 'thisBrandOnly',
                'rateSearchForm.redemptionSearch':'false',
                'rateSearchForm.checkinDate': self.check_in,
                'rateSearchForm.checkoutDate': self.check_out,
                'rateSearchForm.viewAllRates':'true',
                'rateSearchForm.forcedHotelSearch':'true',
                'rateSearchForm.hotelCode':'ONTORAIR',
                'rateSearchForm.numberRooms':'1',
                'rateSearchForm.o[0].a':'1',
                'rateSearchForm.o[0].c':'0',
                'rateSearchForm.o[1].a':'1',
                'rateSearchForm.o[1].c':'0',
                'rateSearchForm.o[2].a':'1',
                'rateSearchForm.o[2].c':'0',
                'rateSearchForm.o[3].a':'1',
                'rateSearchForm.o[3].c':'0',
                'rateSearchForm.o[4].a':'1',
                'rateSearchForm.o[4].c':'0',
                'rateSearchForm.o[5].a':'1',
                'rateSearchForm.o[5].c':'0',
                'rateSearchForm.o[6].a':'1',
                'rateSearchForm.o[6].c':'0',
                'rateSearchForm.o[7].a':'1',
                'rateSearchForm.o[7].c':'0',
                'rateSearchForm.o[8].a':'1',
                'rateSearchForm.o[8].c':'0',
                'rateSearchForm.rmcCode':'',
                'rateSearchForm.ecertCode':'',
                'rateSearchForm.promotionalCode':'',
                'rateSearchForm.corporateAccountID':'',
                'rateSearchForm.travelAgencyId':''
            },
            callback=self.after_post
        )]

    def after_post(self, response):
        open_in_browser(response)
        sel = Selector(response)

        # TODO: How to extract just the first element?
        rooms = sel.css('.rateinfo')
        hotel = sel.css('.RADhotelname::text')

        available = False

        if rooms:
            available = True

        if not hotel:
            # log something
            pass

        name = hotel[0].extract().strip()
        hotel = '{hotel}'.format(hotel=self.name)

        item = Hotel()
        item['name'] = hotel
        item['available'] = available
        item['last_updated'] = datetime.now()

        return item