from hoteltracker import HotelWebsite

class Marriott(HotelWebsite):
    def __init__(self, *args, **kwargs):
        default_args = {
            'name': 'Marriott Toronto Airport',
            'short_name': 'Marriott',
            'parameters': {
                'arrival': {
                    'name': 'checkinDate',
                    'type': 'date'
                },
                'departure': {
                    'name': 'checkoutDate',
                    'type': 'date'
                }
            },
            'formats': {
                'date': '%d/%m/%Y'
            },
            'conditions': [{
                'selector': '_text',
                'pattern': '.*The cut-off date has passed. Access codes for this event have expired.*',
                'found': False
            }, {
                'selector': '???',
                'pattern': '', # Unused
                'found': True
            }],
            'pages': [{
                'url': 'https://resweb.passkey.com/Resweb.do',
                'GET': {
                    'mode': 'welcome_ei_new',
                    'eventID': '10350521'
                }
            }, {
                'url': 'https://resweb.passkey'
                       '.com/ux/LodgingselectPageAction_ux.do',
                'POST': {
                    'pageFrom': 'LodgingDetail',
                    'hdnlocale': 'en',
                    'lodgingType': '0',
                    'searchType': '',
                    'hdndatepattern': 'dd/MM/yy',
                    'calHeader_chkIn': 'Check-in Date:',
                    'calHeader_chkOut': 'Check-Out Date:',
                    'checkinDate': '24/05/2013',
                    'checkoutDate': '26/05/2013',
                    'noOfRooms': '1',
                    'noOfGuests': '1',
                    'groupTypeCode': 'Attendee',
                    'accessCode': '' # Need code!
                }
            }]
        }

        super(Marriott, self).__init__(**default_args)