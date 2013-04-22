from hoteltracker import HotelWebsite

# Sheraton Toronto Airport hotel website is seriously different from other
# Sheraton websites / Starwood Meeting Properties...

# If you need an example site, jsut google the base URL:
#    https://www.starwoodmeeting.com/StarGroupsWeb/
class SheratonTorontoAirport(HotelWebsite):
    def __init__(self, *args, **kwargs):
        default_args = {
            'name': 'Sheraton Toronto Airport',
            'short_name': 'Sheraton',
            'parameters': {
                'arrival': {
                    'name': 'resStartDate',
                    'type': 'date'
                },
                'departure': {
                    'name': 'resEndDate',
                    'type': 'date'
                }
            },
            'formats': {
                'date': '%Y-%m-%d'
            },
            'conditions': [{
                'selector': '_text',
                'pattern': '.*Room unavailable on one or all of your selected dates.*',
                'found': False
            }, {
                # Not 100% if this works.
                'selector': '#resultstable',
                'pattern': '.*Available Rooms.*', # Unused
                'found': True
            }],
            'pages': [{
                'url': 'https://www.starwoodmeeting.com/StarGroupsWeb/booking/reservation',
                'GET': {
                    'id': '1210175516',
                    'key': 'DEEDE'
                }
            }, {
                'url': 'https://www.starwoodmeeting.com/StarGroupsWeb/booking/beginReservation.go',
                'GET': {
                    'com.starwood.mpar.PROPERTY_ID': '3508',
                    'id': '1210175516',
                    'key': 'DEEDE'
                }
            }, {
                'url': 'https://www.starwoodmeeting.com/StarGroupsWeb/booking/checkAvailability.go',
                'POST': {
                    'meetingStartDate': '2013-05-20',
                    'meetingEndDate': '2013-05-30',
                    'com.starwood.mpar.PROPERTY_ID': '3508',
                    'id': '1210175516',
                    'key': 'DEEDE',
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
        }

        super(SheratonTorontoAirport, self).__init__(**default_args)