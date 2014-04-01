from datetime import datetime
from scrapy.selector import Selector
from scrapy.utils.response import open_in_browser
from hoteltracker.items import Hotel
from hoteltracker.spiders.HotelSpider import HotelSpider


class RadissonSpider(HotelSpider):
    name = "Radisson"
    allowed_domains = ["radisson.com"]
    url_template = 'http://www.radisson.com/{0}'
    date_format = '%m/%d/%Y'
    form_css = '[name=rateSearchForm]::attr(action)'

    def populate_params(self):
        return { # TODO: Which of these is critical
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
            'rateSearchForm.promotionalCode': self.group_code,
            'rateSearchForm.corporateAccountID':'',
            'rateSearchForm.travelAgencyId':''
        }

    def has_search_results(self, response):
        sel = Selector(response)
        results = sel.css('.rateinfo')
        return results

    def parse_search_results(self, response):
        return self.create_item(available=True)

    def parse_unknown(self, response):
        return self.create_item()