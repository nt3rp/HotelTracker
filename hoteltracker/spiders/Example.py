from scrapy.spider import Spider
from scrapy.http import FormRequest

class ExampleSpider(Spider):
    name = 'example'
    start_urls = [
        'http://www3.hilton.com/en/hotels/ontario/hilton-toronto-airport-hotel-and-suites-YYZHIHH/index.html'
    ]

    def parse(self, response):
        self.log('Parsing page')
        return [
            FormRequest.from_response(
                response,
                formdata={
                    'departureDate': '13 Apr 2014',
                    'arrivalDate': '11 Apr 2014',
                    'ctyhocn': 'YYZHIHH',
                  '_flexibleDates': 'on',
                  '_rewardBooking': 'on',
                 'numberOfRooms': '1',
                 'numberOfAdults[0]': '1',
                 'numberOfChildren[0]': '0',
                 'numberOfAdults[1]': '1',
                 'numberOfChildren[1]': '0',
                 'numberOfAdults[2]': '1',
                 'numberOfChildren[2]': '0',
                 'numberOfAdults[3]': '1',
                 'numberOfChildren[3]': '0',
                 'promoCode': '',
                 'corporateId': '',
                 '_rememberCorporateId': 'on',
                 '_aaaRate': 'on',
                 '_aarpRate': 'on',
                 '_governmentRate': 'on',
                 '_travelAgentRate': 'on'

                },
                callback=self.after_check
            )
        ]

    def after_check(self, response):
        self.log(response.body)
