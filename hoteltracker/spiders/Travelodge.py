from datetime import datetime
from scrapy.selector import Selector
from scrapy.utils.response import open_in_browser
from hoteltracker.items import Hotel
from hoteltracker.spiders.HotelSpider import HotelSpider


class TravelodgeSpider(HotelSpider):
    name = "Travelodge"
    allowed_domains = ["travelodge.com"]
    url_template = 'http://www.travelodge.com/hotels/{0}/rooms-rates'
    date_format = '%m/%d/%Y'
    use_query_params = True

    def populate_params(self):
        return {
            'checkin_date': self.check_in,
            'checkout_date': self.check_out,
            'rooms': '1',
            'adults': '1',
            'teens': '0',
            'children': '0',
            # What is this param called?
            'rate_code': self.group_code
        }

    def has_search_results(self, response):
        open_in_browser(response)
        sel = Selector(response)

        results = sel.css('.room_info')
        error = sel.css('.error.choose_dates')

        return results and not error

    def parse_search_results(self, response):
        return self.create_item(available=True)

    def parse_unknown(self, response):
        # TODO: Should return an item with availability `False` in this case
        # No rooms: There are no rooms available that match your requested travel criteria. Please consider modifying your preferences or travel dates, or select another hotel nearby
        # Bad code: The Group Code provided does not exist at this hotel. Please check the code and try again. Contact your nearest reservation office for assistance.
        # Missing URL Params: We are sorry, your Group Code cannot be booked on our web site. Please contact the hotel directly call your nearest reservation office for assistance.

        return self.create_item()