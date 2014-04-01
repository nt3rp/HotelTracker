from datetime import datetime
from scrapy.selector import Selector
from scrapy.utils.response import open_in_browser
from hoteltracker.items import Hotel
from hoteltracker.spiders.HotelSpider import HotelSpider


class InternationalPlaza(HotelSpider):
    name = "InternationalPlaza"
    allowed_domains = ["gc.synxis.com"]
    url_template = 'https://gc.synxis.com/rez.aspx'
    date_format = '%Y-%m-%d'
    use_query_params = True

    # https://gc.synxis.com/rez.aspx

    def populate_params(self):
        return {
            'arrive': self.check_in,
            'depart': self.check_out,
            'start': '111', # MAGIC: Remove this and it no longer works
            'rooms': '1',
            'adult': '1',
            'child': '0',
            'hotel': self.location_code,
            'group': self.group_code
        }

    def has_search_results(self, response):
        sel = Selector(response)
        results = sel.css('.ProductsHeader')
        return results

    def parse_search_results(self, response):
        return self.create_item(available=True)

    def parse_unknown(self, response):
        return self.create_item()