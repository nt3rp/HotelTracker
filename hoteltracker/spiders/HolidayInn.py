from datetime import datetime
from scrapy.selector import Selector
from scrapy.utils.response import open_in_browser
from hoteltracker.items import Hotel
from hoteltracker.spiders.HotelSpider import HotelSpider


class HolidayinnSpider(HotelSpider):
    name = "HolidayInn"
    allowed_domains = ["holidayinn.com", "ihg.com"]
    url_template = 'http://www.holidayinn.com/hotels/us/en/{0}/hoteldetail'
    date_format = '%b-%d-%Y'
    form_css = '#hotelDetailsBean::attr(action)'

    def populate_params(self):
        return {
            'adultsCount'   : '1',
            'childrenCount' : '0',
            'roomsCount'    : '1',
            'checkInDate'   : self.check_in,
            'checkOutDate'  : self.check_out,
            'groupCode'     : self.group_code,
            'corporateId'   : ''
        }

    def has_search_results(self, response):
        sel = Selector(response)
        results = sel.css('.ratesListing .roomsView')
        return results

    def parse_search_results(self, response):
        return self.create_item(available=True)

    def parse_unknown(self, response):
        # TODO: Should return an item with availability `False` in this case
        # No rooms: There are no rooms available that match your requested travel criteria. Please consider modifying your preferences or travel dates, or select another hotel nearby
        # Bad code: The Group Code provided does not exist at this hotel. Please check the code and try again. Contact your nearest reservation office for assistance.
        # Missing URL Params: We are sorry, your Group Code cannot be booked on our web site. Please contact the hotel directly call your nearest reservation office for assistance.

        return self.create_item()