# -*- coding: utf-8 -*-
import collections
import contextlib
import cookielib
import json
import logging
import re
import urllib
import urllib2
from bs4 import BeautifulSoup
from datetime import datetime
from hoteltracker.utils import list_missing_args

class HotelWebsite(object):
    REQUIRED_ARGS = ('name', 'pages', 'parameters', 'conditions')

    # TODO: Do we really need kwargs? Why not just define the kwargs?
    def __init__(self, *args, **kwargs):
        if not all(field in kwargs for field in self.REQUIRED_ARGS):
            error = list_missing_args(self.REQUIRED_ARGS, kwargs,
                message='Missing argument{s}: {args}')
            raise ValueError(error)

        for key, value in kwargs.iteritems():
            new_key = '_{key}'.format(key=key)
            setattr(self, new_key, value)

        if not isinstance(self._pages, collections.Iterable):
            raise TypeError('\'self.pages\' is not iterable')

        # Pre-compile condition regexes
        for condition in self._conditions:
            condition['pattern_str'] = condition.get('pattern')
            condition['pattern'] = re.compile(condition.get('pattern'))

        if not all(x in kwargs for x in ('opener', 'cookie_jar')):
            self.__cookie_jar = cookielib.CookieJar()
            cookie_processor = urllib2.HTTPCookieProcessor(self.__cookie_jar)
            self.__opener = urllib2.build_opener(cookie_processor)
        else:
            self.__cookie_jar = kwargs.get('cookie_jar')
            self.__opener = kwargs.get('opener')

        # TODO: Replace calls with `urllib2.urlopen` after urllib
        # .install_opener?

        logger_name = 'hotel_tracker.{0}'.format(self._name)
        self.logger = logging.getLogger(logger_name)
        self.logger.debug('Created new instance')


    def is_available(self, *args, **kwargs):
        if not all(field in kwargs for field in ('arrival', 'departure')):
            raise ValueError('Missing required arguments')
        self.logger.debug('kwargs: {0}'.format(kwargs))

        for page in self._pages:
            self.logger.info('page: {0}'.format(page))

            get = self._convert_params(page.get('GET'), kwargs)
            self.logger.debug('GET: {0}'.format(get))

            post = self._convert_params(page.get('POST'), kwargs)
            self.logger.debug('POST: {0}'.format(post))

            response = self._visit(page, get, post)
            self.logger.debug('Response: {0}'.format(response))

        self.__cookie_jar.clear()
        result = self._analyze_response(response)
        return result

    def _convert_params(self, data, params):
        """Convert `params` to a format the site expects"""
        if not data:
            return params

        for key, value in params.iteritems():
            nonstandard = self._parameters.get(key)
            if nonstandard and nonstandard['name'] in data.keys():
                field = self._format_param(nonstandard.get('type'), value)
                data[nonstandard['name']] = field
        return data

    def _format_param(self, type, value):
        # TODO: Don't create this dictionary every time
        conversions = {
            'date': self._format_date
        }

        try:
            return conversions.get(type)(value)
        except TypeError:
            raise ValueError('Unrecognized conversion type')

    def _format_date(self, str_date):
        original_date = datetime.strptime(str_date, '%Y-%m-%d')
        formatted_date = original_date.strftime(self._formats.get('date', '%Y-%m-%d'))
        return formatted_date

    def _analyze_response(self, response):
        soup = BeautifulSoup(response)

        success = True
        for condition in self._conditions:
            self.logger.debug('Condition: {0}'.format(condition))

            # Right now, only can do tags; not CSS selectors
            # Needs to be more sophisticated
            selector = condition.get('selector')
            pattern = condition.get('pattern')
            found = condition.get('found')

            if selector == "_text":
                selector = True

            result = soup.find(selector, text=pattern)

            if found != bool(result):
                success = False
                break

        return success

    def _visit(self, page, get=None, post=None):
        url = page.get('url')

        # TODO: Verify that no other get params are included
        # Alternatively, parse them out and add them again
        if get:
            url = '{0}?{1}'.format(url, urllib.urlencode(get))

        if post:
            post = urllib.urlencode(post)

        self.logger.debug('URL: {0}'.format(url))
        self.logger.debug('POST: {0}'.format(post))

        with contextlib.closing(self.__opener.open(url, post)) as opener:
            results = opener.read()

        return results

    @classmethod
    def from_json(cls, file):
        with open(file, 'r') as f:
            json_obj = json.loads(f.read())

        return cls(**json_obj)