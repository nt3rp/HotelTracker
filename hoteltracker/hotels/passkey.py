from hoteltracker import HotelWebsite

class Passkey(HotelWebsite):
    def __init__(self, *args, **kwargs):
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

        if kwargs.get('mode'):
            # Use the actual hotel code
            mode = kwargs.get('mode')
        else:
            # TODO: ERROR!
            pass

        if kwargs.get('reservation_type'):
            # Use the actual hotel code
            res_type = kwargs.get('reservation_type')
        else:
            # TODO: ERROR!
            pass

        default_args = {
            'name': name,
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
                    'mode': mode,
                    res_type: hotel
                }
            }, {
                'url': 'https://resweb.passkey.com/ux/LodgingselectPageAction_ux.do',
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

        super(Passkey, self).__init__(**default_args)

class Marriott(Passkey):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(
            name='Marriott Toronto Airport',
            hotel_code='10350521',
            mode='welcome_ei_new',
            reservation_type='eventID'
        )

class CrownePlaza(Passkey):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(
            name='Crowne Plaza Toronto Airport',
            hotel_code='15543280',
            mode='welcome_gi_new',
            reservation_type='groupID'
        )