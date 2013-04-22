from hoteltracker import HotelWebsite

class Radisson(HotelWebsite):
    def __init__(self, *args, **kwargs):
        default_args = {
            'name': 'Radisson Toronto Airport',
            'short_name': 'Radisson',
            'parameters': {
                'arrival': {
                    'name': 'rateSearchForm.checkinDate',
                    'type': 'date'
                },
                'departure': {
                    'name': 'rateSearchForm.checkoutDate',
                    'type': 'date'
                }
            },
            'formats': {
                'date': '%m/%d/%Y'
            },
            'conditions': [{
                'selector': '_text',
                'pattern': '.*there are no rooms available on your requested dates.*',
                'found': False
            }, {
                'selector': 'hotelratesdisplayoptions',
                'pattern': '', # Unused
                'found': True
            }],
            'pages': [{
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
                    'rateSearchForm.ecertCode': 'ANIME',
                    'rateSearchForm.promotionalCode': '',
                    'rateSearchForm.corporateAccountID': '',
                    'rateSearchForm.travelAgencyId': ''
                }
            }]
        }

        super(Radisson, self).__init__(**default_args)