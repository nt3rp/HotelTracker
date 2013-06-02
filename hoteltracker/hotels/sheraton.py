from hoteltracker.hotel import HotelScraper

# Sheraton Toronto Airport hotel website is seriously different from other
# Sheraton websites / Starwood Meeting Properties...

# If you need an example site, jsut google the base URL:
#    https://www.starwoodmeeting.com/StarGroupsWeb/
class StarwoodGroupScraper(HotelScraper):
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get('name', 'Unknown Starwood Group Hotel')
        self.short_name = kwargs.get('short_name', '? Starwood')
        self.hotel_type = kwargs.get('hotel_type', '')
        self.location_code = kwargs.get('location_code')
        self.group_code = kwargs.get('group_code', '')

        self.parameters = {
            'arrival': {
                'name': 'resStartDate',
                'type': 'date'
            },
            'departure': {
                'name': 'resEndDate',
                'type': 'date'
            }
        }

        self.formats = {
            'date': '%Y-%m-%d'
        }

        self.rules = [{
            'selector': '_text',
            'pattern': '.*Room unavailable on one or all of your selected dates.*',
            'found': False
        }, {
            # Not 100% if this works.
            'selector': '#resultstable',
            'pattern': '.*Available Rooms.*', # Unused
            'found': True
        }]

        # Is `id` actually the location id? What is the difference between it
        # and `PROPERTY_ID`?
        self.pages = [{
            'url': 'https://www.starwoodmeeting.com/StarGroupsWeb/booking/reservation',
            'GET': {
                'id': '1210175516',
                'key': self.group_code
            }
        }, {
            'url': 'https://www.starwoodmeeting.com/StarGroupsWeb/booking/beginReservation.go',
            'GET': {
                'com.starwood.mpar.PROPERTY_ID': '3508',
                'id': '1210175516',
                'key': self.group_code
            }
        }, {
            'url': 'https://www.starwoodmeeting.com/StarGroupsWeb/booking/checkAvailability.go',
            'POST': {
                'meetingStartDate': '2013-05-20',
                'meetingEndDate': '2013-05-30',
                'com.starwood.mpar.PROPERTY_ID': '3508',
                'id': '1210175516',
                'key': self.group_code,
                'resStartDate': '2013-05-24',
                'resEndDate': '2013-05-26',
                'numberOfRooms': '01',
                'numberOfAdults': '01',
                'numberOfChildren': '00',
                'childAgeIndexed[0]': '00',
                'childAgeIndexed[1]': '00',
                'childAgeIndexed[2]': '00',
                'bedType': ''
            }
        }]

        super(StarwoodGroupScraper, self).__init__(*args, **kwargs)


class SheratonTorontoAirport(StarwoodGroupScraper):
    def __init__(self, *args, **kwargs):
        super(SheratonTorontoAirport, self).__init__(
            hotel_name='Sheraton Toronto Airport',
#            group_code='DEEDE',
            **kwargs
        )