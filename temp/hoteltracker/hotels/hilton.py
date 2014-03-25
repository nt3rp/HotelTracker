from hoteltracker.hotel import HotelScraper

class HiltonScraper(HotelScraper):
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get('name', 'Unknown Hilton Hotel')
        self.short_name = kwargs.get('short_name', '? Hilton')
        self.hotel_type = kwargs.get('hotel_type', 'hi')
        self.location_code = kwargs.get('location_code')
        self.group_code = kwargs.get('group_code', '')

        base_url = 'https://secure3.hilton.com/en_US/{0}/reservation/book.htm'
        url = base_url.format(self.hotel_type)

        self.parameters = {
            'arrival': {
                'name': 'arrivalDate',
                'type': 'date'
            },
            'departure': {
                'name': 'departureDate',
                'type': 'date'
            }
        }

        self.formats = {
            'date': '%d %b %Y'
        }

        self.rules = [{
            'selector': '_text',
            'pattern': '.*The requested rate is not available.*',
            'found': False
        }, {
            'selector': 'title',
            'pattern': '.*Available Rooms.*',
            'found': True
        }]

        # TODO: Which parameters are actually required?
        self.pages = [{
            'url': url,
            'POST': {
                'ctyhocn': self.location_code
            }
        }, {
            'url': url,
            'GET': {
                'execution': 'e1s1'
            },
            'POST': {
                'arrivalDate': '25 May 2012',
                'departureDate': '27 May 2012',
                '_flexibleDates': 'on',
                '_rewardBooking': 'on',
                'numberOfRooms': '1',
                'numberOfAdults[0]': '1',
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
                'groupCode': self.group_code,
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

        super(HiltonScraper, self).__init__(*args, **kwargs)


class DoubletreeInternationalPlaza(HiltonScraper):
    def __init__(self, *args, **kwargs):
        super(DoubletreeInternationalPlaza, self).__init__(
            name='DoubleTree International',
            location_code='YYZIPDT',
#            group_code='ANM',
            hotel_type='dt',
            **kwargs
        )

class HiltonTorontoAirport(HiltonScraper):
    def __init__(self, *args, **kwargs):
        super(HiltonTorontoAirport, self).__init__(
            name='Hilton Toronto Airport',
            location_code='YYZHIHH',
#            group_code='ANIM13',
            hotel_type='hi',
            **kwargs
        )


class HiltonGardenInnTorontoAirport(HiltonScraper):
    def __init__(self, *args, **kwargs):
        super(HiltonGardenInnTorontoAirport, self).__init__(
            name='Hilton Garden Inn Toronto Airport',
            location_code='YYZTAGI',
#            group_code='ANI',
            hotel_type='gi',
            **kwargs
        )


class HamptonInnSuites(HiltonScraper):
    def __init__(self, *args, **kwargs):
        super(HamptonInnSuites, self).__init__(
            name='Hampton Inn and Suites',
            location_code='YYZHSHX',
#            group_code='V86',
            hotel_type='hp',
            **kwargs
        )
