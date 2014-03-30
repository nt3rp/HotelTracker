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
        'http://www.holidayinn.com/hotels/us/en/toronto/yyzae/hoteldetail',
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