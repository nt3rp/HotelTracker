import json
import logging
import urllib
from datetime import datetime
from pyquery import PyQuery as pq

class HotelWebsite(object):
    """Each hotel knows how to do a few things:
        - check it's availability
    """

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
        logging.info('Creating new HotelWebsite')
        if not all(test in kwargs for test in ('name', 'pages', 'fields')):
            # Is there a simple way that we can both check this, and list the missing field?
            raise ValueError('Missing one of \'name\', \'pages\', or \'fields\'')

        for k, v in kwargs.iteritems():
            var = '_{key}'.format(key=k)
            setattr(self, var, v)
            logging.debug('set HotelWebsite.{0}: {1}'.format(var, v))

        # For now, use a global URL opener
        self.__opener = opener
        logging.debug('set HotelWebsite.__opener: {0}'.format(opener))


    # Private methods
    def _visit_page(self, url, data=None, method=None):
        """ Visits a single page """
        if data:
            data = urllib.urlencode(data)

        #TODO: handle open errors
        if method == 'POST':
            response = self.__opener.open(url, data)
            logging.info('Visited page {0} with {1} params'.format(url, data))
        else:
            url = url + '?' + data
            response = self.__opener.open(url)
            logging.info('Visiting page {0}'.format(url))
        results = response.read()
        logging.debug('_visit_page: response:\n{0}'.format(results))
        response.close()
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

    def _get_results(self, response):
        logging.info('_get_results: Analyzing availability results')
        return response

    # Public methods
    def check_availability(self, **kwargs):
        if not all(test in kwargs for test in ('arrival', 'departure')):
            raise ValueError("Missing arrival or departure time")

        for p in self._pages:
            url_params = self._convert_fields(p.get('data'), **kwargs)
            response = self._visit_page(p.get('url'), url_params, method=p.get('method'))
        results = self._get_results(response)
        return results

    # Static and class methods
    @classmethod
    def from_json_file(cls, opener, file):
        hotels = []
        f_handle = open(file, 'r')
        json_obj = json.loads(f_handle.read())
        f_handle.close()

        for kwargs in json_obj:
            hotels.append(cls(opener, **kwargs))

        return hotels


