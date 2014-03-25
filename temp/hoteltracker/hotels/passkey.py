from hoteltracker import HotelWebsite
from hoteltracker.hotel import HotelScraper

class PasskeyScraper(HotelScraper):
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get('name', 'Unknown Passkey Hotel')
        self.short_name = kwargs.get('short_name', '? Passkey')
        self.hotel_type = kwargs.get('hotel_type', '')
        self.location_code = kwargs.get('location_code')
        self.group_code = kwargs.get('group_code', '')
        self.group_type = kwargs.get('group_type', 'groupID') # Alt. eventID

        # This seems dumb, but is necessary AFAIK
        modes = {
            'eventID': 'welcome_ei_new',
            'groupID': 'welcome_gi_new'
        }

        mode = modes.get(self.group_type)

        self.parameters = {
            'arrival': {
                'name': 'checkinDate',
                'type': 'date'
            },
            'departure': {
                'name': 'checkoutDate',
                'type': 'date'
            }
        }

        self.formats = {
            'date': '%d/%m/%Y'
        }

        self.rules = [{
            'selector': '_text',
            'pattern': '.*The cut-off date has passed. Access codes for this event have expired.*',
            'found': False
        }, {
            'selector': '???', # TODO: Under what conditions does this succeed?
            'pattern': '', # Unused
            'found': True
        }]

        self.pages = [{
            'url': 'https://resweb.passkey.com/Resweb.do',
            'GET': {
                'mode': mode,
                self.group_type: self.location_code
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
                'accessCode': self.group_code # REQUIRED
            }
        }]

        super(PasskeyScraper, self).__init__(*args, **kwargs)


class Marriott(PasskeyScraper):
    def __init__(self, *args, **kwargs):
        super(Marriott, self).__init__(
            name='Marriott Toronto Airport',
            location_code='10350521',
            group_type='eventID',
            **kwargs
        )


class CrownePlaza(PasskeyScraper):
    def __init__(self, *args, **kwargs):
        super(CrownePlaza, self).__init__(
            name='Crowne Plaza Toronto Airport',
            location_code='15543280',
            group_type='groupID',
            **kwargs
        )