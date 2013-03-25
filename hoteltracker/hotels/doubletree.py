from hoteltracker import HotelWebsite

#TODO: For now, just do the Doubletree International Toronto
class Doubletree(HotelWebsite):
    def __init__(self, *args, **kwargs):
        default_args = {
            'name': 'DoubleTree International',
            'short_name': 'DoubleTree',
            'parameters': {
                'arrival': {
                    'name': 'arrivalDate',
                    'type': 'date'
                },
                'departure': {
                    'name': 'departureDate',
                    'type': 'date'
                }
            },
            'formats': {
                'date': '%d %b %Y'
            },
            'conditions': [{
                'selector': '_text',
                'pattern': '.*The requested rate is not available.*',
                'found': False
            }, {
                'selector': 'title',
                'pattern': '.*Available Rooms.*',
                'found': True
            }],
            'pages': [{
                'url': 'https://secure3.hilton.com/en_US/dt/reservation/book.htm',
                'POST': {
                    'ctyhocn': 'YYZIPDT'
                }
            }, {
                'url': 'https://secure3.hilton.com/en_US/dt/reservation/book.htm',
                'GET': {
                    'execution': 'e1s1'
                },
                'POST': {
                    'arrivalDate': '25 May 2012',
                    'departureDate': '27 May 2012',
                    '_flexibleDates': 'on',
                    '_rewardBooking': 'on',
                    'numberOfRooms': '1',
                    'numberOfAdults[0]': '4',
                    'numberOfChildren[0]': '0',
                    'numberOfAdults[1]': '1',
                    'numberOfChildren[1]': '0',
                    'numberOfAdults[2]': '1',
                    'numberOfChildren[2]': '0',
                    'numberOfAdults[3]': '1',
                    'numberOfChildren[3]': '0',
                    'promoCode': '',
                    'srpId': '',
                    'onlineValueRate': '',
                    'groupCode': 'ANM',
                    'corporateId': '',
                    '_rememberCorporateId': 'on',
                    '_aaaRate': 'on',
                    '_aarpRate': 'on',
                    '_governmentRate': 'on',
                    '_travelAgentRate': 'on',
                    '_eventId_findRoom': 'Continue',
                    'execution': 'e5s2'
                }
            }]
        }

        super(Doubletree, self).__init__(**default_args)