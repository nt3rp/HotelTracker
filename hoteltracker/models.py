from collections import deque
import re
import json
import urllib
import logging

from datetime import datetime
from bs4 import BeautifulSoup
import twitter

class HotelWebsite(object):
    """Each hotel knows how to do a few things:
        - check it's availability
    """
    REQUIRED_FIELDS = ('name', 'pages', 'fields', 'conditions')

    def __init__(self, opener, **kwargs):
        """Creates a new HotelWebsite instance.

        Required arguments:
            name        : display name
            pages       : list of pages
            fields      : mapping of standardized to non-standard keys

        Optional arguments:
            formats     : a dictionary of formats for different field types
            short_name  : short version of the display name
        """
        if not all(test in kwargs for test in self.REQUIRED_FIELDS):
            # Is there a simple way that we can both check this, and list the missing field?
            raise ValueError('Missing one of required fields.')

        logging.info('__init__: {0}'.format(kwargs.get('name')))

        for k, v in kwargs.iteritems():
            var = '_{key}'.format(key=k)
            setattr(self, var, v)
            logging.debug('HotelWebsite.{0} = {1}'.format(var, v))

        # Pre-compile condition regexes
        for condition in self._conditions:
            condition['pattern'] = re.compile(condition['pattern'])

        # For now, use a global URL opener
        self.__opener = opener
        logging.debug('HotelWebsite.__opener = {0}'.format(opener))


    # Private methods
    def _visit_page(self, url, data=None, method=None):
        """ Visits a single page """
        if data:
            data = urllib.urlencode(data)

        # Previously, we were doing a get request with parameters
        # ...is this no longer necessary?

        logging.info('_visit_page: url  = {0}'.format(url))
        logging.info('_visit_page: data = {0}'.format(data))

        # Can't do `with` here?
        #     addinfourl instance has no attribute '__exit__'
        response = self.__opener.open(url, data)
        logging.debug('_visit_page: headers = {0}'.format(
            unicode(response.info())
        ))
        results = response.read()
        response.close()

        logging.debug('_visit_page: response = \n{0}'.format(results))
        return results

    def _format_field(self, type, value):
        if type == "date":
            return self._format_date(value)
        else:
            raise ValueError("Unrecognized type")

    def _format_date(self, str_date):
        original_date = datetime.strptime(str_date, '%Y-%m-%d')
        formatted_date = original_date.strftime(self._formats.get('date', '%Y-%m-%d'))
        return formatted_date

    def _convert_fields(self, data, **params):
        for key, value in params.iteritems():
            nonstandard = self._fields.get(key)
            if nonstandard and nonstandard['name'] in data.keys():
                data[nonstandard['name']] = self._format_field(nonstandard['type'], value)
        return data

    def _analyze_page(self, response):
        logging.info('_get_results: {0}'.format(self._name))

        soup = BeautifulSoup(response)

        success = True
        for condition in self._conditions:
            selector = condition.get('selector')
            pattern  = condition.get('pattern')
            found    = condition.get('found')

            if selector == "_text":
                selector = True

            result = soup.find(selector, text=pattern)
            logging.debug('_get_results: soup result = {0}'.format(result))

            if found != bool(result):
                success = False
                break

        return success

    # Public methods
    def is_available(self, **kwargs):
        if not all(test in kwargs for test in ('arrival', 'departure')):
            raise ValueError("Missing arrival or departure time")

        logging.info("check_availability: {0}, {1}".format(
            self._name, kwargs
        ))

        for p in self._pages:
            url_params = self._convert_fields(p.get('data'), **kwargs)
            response = self._visit_page(p.get('url'), url_params, method=p.get('method'))
        result = self._analyze_page(response)
        return result

    # Static and class methods
    @classmethod
    def from_json_file(cls, opener, file):
        hotels = []
        with open(file, 'r') as f_handle:
            json_obj = json.loads(f_handle.read())

        for kwargs in json_obj:
            hotels.append(cls(opener, **kwargs))

        return hotels


class TwitterHotelMessager(object):
    def __init__(self, json_path=None, atoken=None, asecret=None,
                 ctoken=None, csecret=None):
        if json_path:
            with open(json_path, 'r') as f:
                obj    = json.loads(f.read())
                atoken  = obj.get('access_token')
                asecret = obj.get('access_secret')
                ctoken  = obj.get('consumer_token')
                csecret = obj.get('consumer_secret')

        # Twitter API code
        self._api = twitter.Api(consumer_key=ctoken, consumer_secret=csecret,
            access_token_key=atoken, access_token_secret=asecret)

        if not self._api.VerifyCredentials():
            raise ValueError("Could not connect to Twitter")

        logging.info("__init__: Twitter credentials verified")

        # Hotel code
        self._hotels = {}

    # Private functions
    def _get_state(self, info, now=datetime.now()):
        return {
            'stale'  : self.is_stale(info['last_update'], now=now),
            'changed': self.is_changed(*info['last_results'])
        }

    def _update_info(self, hotel, success, now=datetime.now()):
        info = self._hotels.get(hotel, {
            'last_update': None,
            'last_results': deque([], maxlen=2),
            'name': hotel
        })
        info['last_results'].append(success)
        self._hotels[hotel] = info
        return self._hotels[hotel]

    def _post(self, info, message):
        success = list(info['last_results'])[-1]

        if success:
            num_rooms = "at least one room"
        else:
            num_rooms = "no rooms"

        f_message = message.format(hotel=info['name'], num_rooms=num_rooms)
        logging.info(f_message)
        self._api.PostUpdate(f_message)


    def _post_stale(self, info):
        self._post(info, "{hotel}: Sorry, still {num_rooms} available")

    def _post_changed(self, info):
        self._post(info, "{hotel}: {num_rooms} available")

    # Public functions
    def update(self, hotel, success):
        now   = datetime.now()
        info  = self._update_info(hotel, success, now)

        state = self._get_state(info, now)
        if state['changed'] or not info['last_update']:
            self._post_changed(info)
            info['last_update'] = now
        elif state['stale']:
            self._post_stale(info)
            info['last_update'] = now
        else:
            logging.info("update: No need to update")

    # Static and class methods
    @staticmethod
    def is_changed(prev=False, next=False):
        return prev != next

    @staticmethod
    def is_stale(last_update, now=datetime.now(), stale_duration=14400):
        if not last_update:
            return False
        return (now - last_update).seconds >= stale_duration