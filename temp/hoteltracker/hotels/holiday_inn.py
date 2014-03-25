from hoteltracker import HotelWebsite
from hoteltracker.hotel import HotelScraper

class IHGGroupScraper(HotelScraper):
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get('name', 'Unknown IHG Group Hotel')
        self.short_name = kwargs.get('short_name', '? IHG Group')
        self.hotel_type = kwargs.get('hotel_type', 'holidayinn')
        self.location_code = kwargs.get('location_code')
        self.group_code = kwargs.get('group_code', '')

        website = 'http://www.ihg.com'
        base_path = 'hotels/us/en/'

        self.parameters = {
            'arrival': {
                'name': 'checkInDate',
                'type': 'date'
            },
            'departure': {
                'name': 'checkOutDate',
                'type': 'date'
            }
        }

        self.formats = {
            'date': '%b-%d-%Y'
        }

        self.rules = [{
            'selector': '_text',
            'pattern': '.*There are no rooms available for your requested travel criteria.*',
            'found': False
        }, {
            'selector': '.ratesListing .roomEntry',
            'pattern': '.*',
            'found': True
        }]

        # For whatever reason, we need to visit the same page twice; I think
        # the first time is to just set a cookie...
        page = {
            'url': '{0}{1}{2}/bookthishotel'.format(
                website, base_path, self.location_code
            ),
            'POST': {
                "parentController": "{0}{1}/hoteldetail".format(
                    base_path, self.location_code
                ),
                "includedView": "bookthishotel",
                "checkInDate": "Apr-01-2013",
                "checkOutDate": "Apr-02-2013",
                "adultsCount": "1",
                "childrenCount": "0",
                "roomsCount": "1",
                "groupCode": self.group_code,
                "corporateId": "",
                "ratePreference": "6CBARC"
            }
        }

        self.pages = [page, page]

        super(IHGGroupScraper, self).__init__(*args, **kwargs)


class HolidayInnAirportEast(IHGGroupScraper):
    def __init__(self, *args, **kwargs):
        super(HolidayInnAirportEast, self).__init__(
            name='Holiday Inn Airport - East',
            location_code='toronto/yyzae',
#            group_code='missing group code',
            hotel_type='holidayinn',
            **kwargs
        )

class HolidayInnTorontoInternational(IHGGroupScraper):
    def __init__(self, *args, **kwargs):
        super(HolidayInnTorontoInternational, self).__init__(
            name='Holiday Inn Toronto International',
            location_code='toronto/yyzia',
#            group_code='AEN',
            hotel_type='holidayinn',
            **kwargs
        )

class HotelIndigoTorontoAirport(IHGGroupScraper):
    def __init__(self, *args, **kwargs):
        super(HotelIndigoTorontoAirport, self).__init__(
            name='Hotel Indigo Toronto Airport',
            location_code='toronto/yyzin',
#            group_code='ANN',
            hotel_type='hotelindigo',
            **kwargs
        )