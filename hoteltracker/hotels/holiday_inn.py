from hoteltracker import HotelWebsite

# TODO: Refactor this shit
class HolidayInn(HotelWebsite):
    def __init__(self, *args, **kwargs):

        website = 'http://www.ihg.com'
        base_path = 'hotels/us/en/'

        if kwargs.get('hotel_type'):
            # Use the actual hotel code
            hotel_type = kwargs.get('hotel_type')
        else:
            # TODO: ERROR!
            pass

        if kwargs.get('hotel_code'):
            # Use the actual hotel code
            hotel = kwargs.get('hotel_code')
        else:
            # TODO: ERROR!
            pass

        if kwargs.get('name'):
            name = kwargs.get('name')
        else:
            # TODO: ERROR?
            pass

        if kwargs.get('group_code'):
            group_code = kwargs.get('group_code')
        else:
            group_code = ''

        base_path = '/{0}/{1}'.format(hotel_type, base_path)

        # For whatever reason, we need to visit the same page twice; I think
        # the first time is to just set a cookie...
        page = {
            'url': '{0}{1}{2}/bookthishotel'.format(website, base_path,
                hotel),
            'POST': {
                "parentController": "{0}{1}/hoteldetail".format(base_path, hotel),
                "includedView": "bookthishotel",
                "checkInDate": "Apr-01-2013",
                "checkOutDate": "Apr-02-2013",
                "adultsCount": "1",
                "childrenCount": "0",
                "roomsCount": "1",
                "groupCode": group_code,
                "corporateId": "",
                "ratePreference": "6CBARC"
            }
        }

        default_args = {
            'name': name,
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
                'selector': '.ratesListing .roomEntry',
                'pattern': '.*',
                'found': True
            }],
            'pages': [page, page]
        }

        super(HolidayInn, self).__init__(*args, **default_args)

class HolidayInnAirportEast(HolidayInn):
    def __init__(self):
        super(HolidayInnAirportEast, self).__init__(
            name='Holiday Inn Airport - East',
            hotel_code='toronto/yyzae',
            hotel_type='holidayinn')
            # Need group code...

class HolidayInnTorontoInternational(HolidayInn):
    def __init__(self):
        super(HolidayInnTorontoInternational, self).__init__(
            name='Holiday Inn Toronto International',
            hotel_code='toronto/yyzia',
            group_code='AEN',
            hotel_type='holidayinn')

class HotelIndigoTorontoAirport(HolidayInn):
    def __init__(self):
        super(HotelIndigoTorontoAirport, self).__init__(
            name='Hotel Indigo Toronto Airport',
            hotel_code='toronto/yyzin',
            group_code='ANN',
            hotel_type='hotelindigo')