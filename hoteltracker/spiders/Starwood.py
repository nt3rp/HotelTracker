from datetime import datetime
from scrapy.selector import Selector
from scrapy.utils.response import open_in_browser
from hoteltracker.items import Hotel
from hoteltracker.spiders.HotelSpider import HotelSpider


class StarwoordSpider(HotelSpider):
    name = "Starwood"
    allowed_domains = ["starwoodhotels.com"]

    # TODO: Sheraton should not be part of the template
    # Since we have no other examples though, this is fine
    url_template = 'http://www.starwoodhotels.com/sheraton/rates/rate.html'
    date_format = '%Y-%m-%d'
    use_query_params = True

    # Appear in list of rate preferences
    #   ANIM, ANIME, ANIM2014, DEEDE, CGANIM, ANE20A, ANI

    # DON'T appear in list of rate preferences
    #   ANM, ANN, AHO
    def populate_params(self):
        params = {
            'propertyID': self.location_code, #3508
            'departureDate': self.check_out,
            'arrivalDate': self.check_in,
            #'lengthOfStay': '1',
            'numberOfRooms': '1',
            'numberOfAdults': '1',
            'numberOfChildren': '0',
            # rp: rate plan; pc: promotional code
            'rp': 'PC:{0}'.format(self.group_code)
        }

        if not self.group_code:
            del params['rp']

        return params

    def has_search_results(self, response):
        open_in_browser(response)
        sel = Selector(response)
        results = sel.css('.roomRateBlock')
        return results

    def parse_search_results(self, response):
        return self.create_item(available=True)

    def parse_unknown(self, response):
        return self.create_item()