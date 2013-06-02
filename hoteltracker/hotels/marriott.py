from hoteltracker import HotelWebsite
from hoteltracker.hotel import HotelScraper

class MarriottScraper(HotelScraper):
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get('name', 'Unknown Marriott Hotel')
        self.short_name = kwargs.get('short_name', '? Marriott')
        self.location_code = kwargs.get('location_code')
        self.group_code = kwargs.get('group_code', '')

        self.parameters = {
            'arrival': {
                'name': 'fromDate',
                'type': 'date'
            },
            'departure': {
                'name': 'toDate',
                'type': 'date'
            }
        }

        self.formats = {
            'date': '%m/%d/%Y'
        }

        self.rules = [{
            'selector': '_text',
            'pattern': '.*Group Rate Not Available for Requested Dates.*',
            'found': False
        }, {
            'selector': '#roomRatesSelectionForm',
            'pattern': '.*',
            'found': True
        }]

        # TODO: Which parameters are actually required?
        self.pages = [{
            'url': 'http://www.marriott.com/reservation/availabilitySearch.mi',
            'GET': {
                'propertyCode': self.hotel_code
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
                'groupCode': self.group_code,
                'btn-submit': '',
                'sSubmit': 'Search',
                'miniStoreAvailabilitySearch': 'false',
                'section': 'availability',
                'sSubmit': 'Search'
            }
        }]

        super(MarriottScraper, self).__init__(*args, **kwargs)


class ResidenceInn(MarriottScraper):
    def __init__(self, *args, **kwargs):
        super(ResidenceInn, self).__init__(
            location_code='yyzri',
#            group_code='annanna',
            name='Residence Inn',
            **kwargs
        )

class CourtyardTorontoAirport(MarriottScraper):
    def __init__(self, *args, **kwargs):
        super(CourtyardTorontoAirport, self).__init__(
            location_code='yyzap',
#            group_code='aniania',
            name='Courtyard Toronto Airport',
            **kwargs
        )