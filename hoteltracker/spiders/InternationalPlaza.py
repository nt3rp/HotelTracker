from datetime import datetime
from scrapy.selector import Selector
from scrapy.utils.response import open_in_browser
from hoteltracker.items import Hotel
from hoteltracker.spiders.HotelSpider import HotelSpider


class InternationalPlaza(HotelSpider):
    name = "InternationalPlaza"
    allowed_domains = ["www.internationalplazahotel.com", "gc.synxis.com"]
    url_template = 'http://www.internationalplazahotel.com/'
    date_format = '%m/%d/%Y'
    form_css = '.reservations::attr(action)'

    # https://gc.synxis.com/rez.aspx

    def populate_search_form(self):
        return {
             'checkin': self.check_in,
             'nights': '2',
             'rooms': '1',
             'adults': '1',
             'children': '0',
             'group': self.group_code
        }

    def has_search_results(self, response):
        open_in_browser(response)
        sel = Selector(response)
        results = sel.css('.ProductsHeader')
        return results

    def parse_search_results(self, response):
        return self.create_item(available=True)

    def parse_unknown(self, response):
        return self.create_item()