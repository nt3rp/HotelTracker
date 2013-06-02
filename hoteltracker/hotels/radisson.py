from hoteltracker import HotelWebsite
from hoteltracker.hotel import HotelScraper

# TODO: Update with other carlson rezidor hotels
class CarlsonRezidorScraper(HotelScraper):
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get('name', 'Unknown Carlson-Rezidor Hotel')
        self.short_name = kwargs.get('short_name', '? Carlson-Rezidor')
        self.hotel_type = kwargs.get('hotel_type', '')
        self.location_code = kwargs.get('location_code')
        self.group_code = kwargs.get('group_code', '')

        self.parameters = {
            'arrival': {
                'name': 'rateSearchForm.checkinDate',
                'type': 'date'
            },
            'departure': {
                'name': 'rateSearchForm.checkoutDate',
                'type': 'date'
            }
        }

        self.formats = {
            'date': '%m/%d/%Y'
        }

        self.rules = [{
            'selector': '_text',
            'pattern': '.*there are no rooms available on your requested dates.*',
            'found': False
        }, {
            'selector': 'hotelratesdisplayoptions', #TODO: What is this? cls?
            'pattern': '', # Unused
            'found': True
        }]

        self.pages = [{
            'url': 'http://www.radisson.com/toronto-hotel-on-m9w1j1/ontorair'
        }, {
            'url': 'http://www.radisson.com/reservation/rateSearch.do',
            'POST': {
                'rateSearchForm.crossBrandSearch': '',
                'rateSearchForm.redemptionSearch': 'false',
                'rateSearchForm.checkinDate': '05/24/2013',
                'rateSearchForm.checkoutDate': '05/26/2013',
                'rateSearchForm.viewAllRates': 'true',
                'rateSearchForm.hotelCode': 'ONTORAIR',
                'rateSearchForm.numberRooms': '1',
                'rateSearchForm.o[0].a': '1',
                'rateSearchForm.o[0].c': '0',
                'rateSearchForm.o[1].a': '1',
                'rateSearchForm.o[1].c': '0',
                'rateSearchForm.o[2].a': '1',
                'rateSearchForm.o[2].c': '0',
                'rateSearchForm.o[3].a': '1',
                'rateSearchForm.o[3].c': '0',
                'rateSearchForm.o[4].a': '1',
                'rateSearchForm.o[4].c': '0',
                'rateSearchForm.o[5].a': '1',
                'rateSearchForm.o[5].c': '0',
                'rateSearchForm.o[6].a': '1',
                'rateSearchForm.o[6].c': '0',
                'rateSearchForm.o[7].a': '1',
                'rateSearchForm.o[7].c': '0',
                'rateSearchForm.o[8].a': '1',
                'rateSearchForm.o[8].c': '0',
                'rateSearchForm.rmcCode': 'LOWESTWB',
                'rateSearchForm.ecertCode': self.group_code,
                'rateSearchForm.promotionalCode': '',
                'rateSearchForm.corporateAccountID': '',
                'rateSearchForm.travelAgencyId': ''
            }
        }]

        super(CarlsonRezidorScraper, self).__init__(*args, **kwargs)


class RadissonTorontoAirport(CarlsonRezidorScraper):
    def __init__(self, *args, **kwargs):
        super(RadissonTorontoAirport, self).__init__(
            name='Radisson Toronto Airport',
#            group_code='ANIME',
            **kwargs
        )