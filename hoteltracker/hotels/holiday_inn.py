from hoteltracker import HotelWebsite

#TODO: For now, just do the Holiday Inn Airport East Toronto
class HolidayInn(HotelWebsite):
    def __init__(self, *args, **kwargs):
        default_args = {
            'name': 'Holiday Inn Airport - East',
            'short_name': 'HolidayInn',
            'parameters': {
                'arrival': {
                    'name': 'checkInDt',
                    'type': 'date'
                },
                'departure': {
                    'name': 'checkOutDt',
                    'type': 'date'
                }
            },
            'formats': {
                'date': '%b-%d-%Y'
            },
            'conditions': [{
                'selector': '_text',
                'pattern': '.*There are no rooms available for your requested travel criteria.*',
                'found': False
            }, {
                'selector': 'title',
                # Needs to be a `.ratesListing` inside a `.simpleRate`
                'pattern': '.*Available Rooms.*',
                'found': True
            }],
            'pages': [{
                'url': 'http://www.ihg.com/holidayinn/hotels/us/en/reservation/roomrate',
                'GET': {
                    'execution': 'e1s1',
                    'hotelCode': 'yyzae',
                    'numberOfRooms': '1',
                    'numberOfAdults': '1',
                    'ratePreference': '6CBARC',
                    'numberOfChildren': '0',
                    'execute': 'basic'
                }
            }, {
                'url': 'http://www.ihg.com/holidayinn/hotels/us/en/reservation/roomrate',
                'POST': {
                    'execution': 'e1s1',
                    'hotelCode': 'yyzae',
                    'ratePreference': '6CBARC',
                    'adultsCount': '1',
                    'childrenCount': '0',
                    'roomsCount': '1',
                    'execute': 'basic',
                    'actionName': 'modifySearch',
                    'modifySearch': 'yourRate'
                }
            }]
        }

        super(HolidayInn, self).__init__(**default_args)