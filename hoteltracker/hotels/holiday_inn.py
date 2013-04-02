from hoteltracker import HotelWebsite

#TODO: For now, just do the Holiday Inn Airport East Toronto
class HolidayInn(HotelWebsite):
    def __init__(self, *args, **kwargs):
        default_args = {
            'name': 'Holiday Inn Airport - East',
            'short_name': 'HolidayInn',
            'parameters': {
                'arrival': {
                    'name': 'checkInDate',
                    'type': 'date'
                },
                'departure': {
                    'name': 'checkOutDate',
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
                'selector': '.ratesListing',
                # Needs to be a `.ratesListing` inside a `.simpleRate`
                'pattern': '.*Available Rooms.*',
                'found': True
            }],
            'pages': [{
                'url': 'http://www.ihg.com/holidayinn/hotels/us/en/toronto/yyzae/bookthishotel',
                'POST': {
                    "parentController": "/holidayinn/hotels/us/en/toronto/yyzae/hoteldetail",
                    "includedView": "bookthishotel",
                    "checkInDate": "Apr-01-2013",
                    "checkOutDate": "Apr-02-2013",
                    "adultsCount": "1",
                    "childrenCount": "0",
                    "roomsCount": "1",
                    "groupCode": "", #Need Group Code!
                    "corporateId": "",
                    "ratePreference": "6CBARC"
                }
            }, {
                'url': 'http://www.ihg.com/holidayinn/hotels/us/en/toronto/yyzae/bookthishotel',
                'POST': {
                    "parentController": "/holidayinn/hotels/us/en/toronto/yyzae/hoteldetail",
                    "includedView": "bookthishotel",
                    "checkInDate": "Apr-01-2013",
                    "checkOutDate": "Apr-02-2013",
                    "adultsCount": "1",
                    "childrenCount": "0",
                    "roomsCount": "1",
                    "groupCode": "", #Group Code!
                    "corporateId": "",
                    "ratePreference": "6CBARC"
                }
            }]
        }

        super(HolidayInn, self).__init__(**default_args)