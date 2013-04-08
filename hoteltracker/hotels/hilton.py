from hoteltracker import HotelWebsite


class Hilton(HotelWebsite):
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

        if kwargs.get('hotel_type'):
            type = kwargs.get('hotel_type')
        else:
            # TODO: ERROR!
            pass

        if kwargs.get('group_code') is not None:
            code = kwargs.get('group_code')
        else:
            # TODO: ERROR?
            pass

        root_url = 'https://secure3.hilton.com/en_US/{0}/reservation/book' \
                   '.htm'.format(type)

        default_args = {
            'name': name,
            'short_name': 'Hilton',
            'parameters': {
                'arrival': {
                    'name': 'arrivalDate',
                    'type': 'date'
                },
                'departure': {
                    'name': 'departureDate',
                    'type': 'date'
                }
            },
            'formats': {
                'date': '%d %b %Y'
            },
            'conditions': [{
                'selector': '_text',
                'pattern': '.*The requested rate is not available.*',
                'found': False
            }, {
                'selector': 'title',
                'pattern': '.*Available Rooms.*',
                'found': True
            }],
            'pages': [{
                'url': root_url,
                'POST': {
                    'ctyhocn': hotel
                }
            }, {
                'url': root_url,
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
                    'groupCode': code,
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
        }

        super(Hilton, self).__init__(**default_args)


class DoubletreeInternationalPlaza(Hilton):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(
            name='DoubleTree International',
            hotel_code='YYZIPDT',
            group_code='ANM',
            hotel_type='dt'
        )

class HiltonTorontoAirport(Hilton):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(
            name='DoubleTree International',
            hotel_code='YYZHIHH',
            group_code='ANIM13',
            hotel_type='hi'
        )


class HiltonGardenInnTorontoAirport(Hilton):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(
            name='Hilton Garden Inn Toronto Airport',
            hotel_code='YYZTAGI',
            group_code='ANI',
            hotel_type='gi'
        )