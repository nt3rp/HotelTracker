from hoteltracker import HotelWebsite

class Marriott(HotelWebsite):
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

        if kwargs.get('group_code'):
            group_code = kwargs.get('group_code')
        else:
            group_code = ''

        default_args = {
            'name': name,
            'short_name': 'Marriott',
            'parameters': {
                'arrival': {
                    'name': 'fromDate',
                    'type': 'date'
                },
                'departure': {
                    'name': 'toDate',
                    'type': 'date'
                }
            },
            'formats': {
                'date': '%m/%d/%Y'
            },
            'conditions': [{
                'selector': '_text',
                'pattern': '.*Group Rate Not Available for Requested Dates.*',
                'found': False
            }, {
                'selector': '#roomRatesSelectionForm',
                'pattern': '.*',
                'found': True
            }],
            'pages': [{
                'url': 'http://www.marriott.com/reservation/availabilitySearch.mi',
                'GET': {
                    'propertyCode': hotel
                },
            }, {
                'url': 'http://www.marriott.com/reservation/availabilitySearch.mi',
                'GET': {
                    'isSearch': 'false'
                },
                'POST': {
                    'accountId': '',
					'flexibleDateSearch': 'false',
					'flexibleDates': 'false',
					'fromDate': '05/24/13',
					'minDate': '04/19/2013',
					'maxDate': '04/06/2014',
					'monthNames': 'January,February,March,April,May,June,July,August,September,October,November,December',
					'weekDays': 'S,M,T,W,T,F,S',
					'dateFormatPattern': 'MM/dd/yy',
					'lengthOfStay': '2',
					'toDate': '05/26/13',
					'populateTodateFromFromDate': 'true',
					'defaultToDateDays': '1',
					'numberOfNights': '1',
					'numberOfRooms': '1',
					'numberOfGuests': '1',
					'marriottRewardsNumber': '',
					'useRewardsPoints': 'false',
					'corporateCode': '',
					'displayableIncentiveType_Number': '',
					'clusterCode': 'group',
					'groupCode': group_code,
					'btn-submit': '',
					'sSubmit': 'Search',
					'miniStoreAvailabilitySearch': 'false',
					'section': 'availability',
                    'sSubmit': 'Search'
                }
            }]
        }

        super(Marriott, self).__init__(*args, **default_args)

class ResidenceInn(Marriott):
    def __init__(self):
        super(ResidenceInn, self).__init__(
            hotel_code='yyzri',
            group_code='annanna',
            name='Residence Inn'
        )

class CourtyardTorontoAirport(Marriott):
    def __init__(self):
        super(CourtyardTorontoAirport, self).__init__(
            hotel_code='yyzap',
            group_code='aniania',
            name='Courtyard Toronto Airport'
        )