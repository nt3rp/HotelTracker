from datetime import datetime
from scrapy.http import FormRequest
from scrapy.selector import Selector
from scrapy.spider import Spider
from scrapy.utils.response import open_in_browser
from hoteltracker.items import Hotel


class HolidayinnSpider(Spider):
    name = "HolidayInn"
    allowed_domains = ["holidayinn.com", "ihg.com"]

    # TODO: How can we pass in / use settings to define the start url?
    start_urls = (
        'http://www.holidayinn.com/hotels/us/en/toronto/yyzae/hoteldetail?qAdlt=1&qBrs=6c.hi.ex.rs.ic.cp.in.sb.cw.cv&qChld=0&qFRA=1&qGRM=0&qGrpCd=ANN&qIta=99801505&qPSt=0&qRRSrt=rt&qRms=1&qRpn=1&qRpp=10&qSHp=1&qSmP=3&qSrt=sBR&qWch=0&srb_u=1&icdv=99801505',
        )

    def parse(self, response):
        sel = Selector(response)
        urls = sel.css('#hotelDetailsBean::attr(action)')

        if not urls:
            # log something
            pass

        url = urls[0].extract()

        return [FormRequest(
            url=url,
            formdata={
                'adultsCount'   : '1',
                'childrenCount' : '0',
                'roomsCount'    : '1',
                'checkInDate'   : 'May-23-2014',
                'checkOutDate'  : 'May-25-2014',
                'groupCode'     : 'ANN',
                'corporateId'   : ''
            },
            callback=self.after_post
        )]

    def after_post(self, response):
        sel = Selector(response)

        open_in_browser(response)

        # TODO: How to extract just the first element?
        rooms = sel.css('.ratesListing .roomsView')
        hotel = sel.css('.sel_hoteldetail_link::attr(title)')

        available = False

        if rooms:
            available = True

        if not hotel:
            # log something
            pass

        name = hotel[0].extract()

        item = Hotel()
        item['name'] = name # TODO: Add Hotel name
        item['available'] = available
        item['last_updated'] = datetime.now()

        return item