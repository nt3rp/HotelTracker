from time import strftime, strptime
from datetime import datetime
from scrapy.http import FormRequest
from scrapy.selector import Selector
from scrapy.spider import Spider
from scrapy.utils.response import open_in_browser
from hoteltracker.items import Hotel


class HolidayinnSpider(Spider):
    name = "HolidayInn"
    allowed_domains = ["holidayinn.com", "ihg.com"]
    url_template = 'http://www.holidayinn.com/hotels/us/en/{0}/hoteldetail'
    time_format = '%b-%d-%Y'

    def __init__(self, location_code=None, check_in=None, check_out=None):
        if not location_code:
            location_code = 'toronto/yyzae'

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
                'checkInDate'   : self.check_in,
                'checkOutDate'  : self.check_out,
                'groupCode'     : '',
                'corporateId'   : ''
            },
            callback=self.after_post
        )]

    def after_post(self, response):
        sel = Selector(response)

        search_form = sel.css('#hotelDetailsBean')

        # TODO: Do we care what happens if we're back on the search page?
        # TODO: Should return an item with availability `False` in this case
        if search_form:
            # No rooms: There are no rooms available that match your requested travel criteria. Please consider modifying your preferences or travel dates, or select another hotel nearby
            # Bad code: The Group Code provided does not exist at this hotel. Please check the code and try again. Contact your nearest reservation office for assistance.
            # Missing URL Params: We are sorry, your Group Code cannot be booked on our web site. Please contact the hotel directly call your nearest reservation office for assistance.

            return []

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
        hotel = '{hotel} - {location}'.format(hotel=self.name, location=name)

        item = Hotel()
        item['name'] = hotel
        item['available'] = available
        item['last_updated'] = datetime.now()

        return item