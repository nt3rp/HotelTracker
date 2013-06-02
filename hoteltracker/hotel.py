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
import soupselect
from datetime import datetime
from hoteltracker.utils import list_missing_args

soupselect.monkeypatch()

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

            get = page.get('GET')
            if get:
                get = self._convert_params(get, kwargs)

            self.logger.debug('GET: {0}'.format(get))

            post = page.get('POST')
            if post:
                post = self._convert_params(post, kwargs)

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

            selector = condition.get('selector')
            pattern = condition.get('pattern')
            found = condition.get('found')

            if selector == "_text":
                result = soup.find(text=pattern)
            else:
                result = soup.findSelect(selector)

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

# TODO: Create a 'page' interface / class
# ... could just be a named tuple

class HotelScraper(object):
    """A low-level scraper intended for checking hotel availability."""

    def __init__(self, opener=None, cookie_jar=None, *args, **kwargs):
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

        self.cookie_jar = cookie_jar
        if not self.cookie_jar:
            self.cookie_jar = cookielib.CookieJar()

        # We assume that the opener and provided cookie_jar
        # are connected.
        self.opener = opener
        if not self.opener:
            self.opener = urllib2.build_opener(
                urllib2.HTTPCookieProcessor(self.cookie_jar)
            )

    # TODO: Allow other criteria
    def is_available(self, arrival, departure, *args, **kwargs):
        if not all([arrival, departure]):
            # TODO: ERROR
            pass

        criteria = {
            'arrival': arrival,
            'departure': departure
        }

        for page in self.pages:
            get = page.get('GET')
            if get:
                get = self.normalize_params(get, criteria)

            post = page.get('POST')
            if post:
                get = self.normalize_params(post, criteria)

            url = page.get('url')
            html = self.visit(url, get, post)

        is_available = self.analyze_response()
        self.cookie_jar.clear()
        return is_available

    def visit(self, url, get=None, post=None):
        """
        Visits the given url.
        """
        if get:
            url = '{0}?{1}'.format(url, urllib.urlencode(get))

        if post:
            post = urllib.urlencode(post)

        with contextlib.closing(self.opener.open(url, post)) as opener:
            html = opener.read()

        return html

    def analyze_response(self, html):
        soup = BeautifulSoup(html)

        success = True
        for rule in self.rules:

            selector = rule.get('selector')
            pattern = rule.get('pattern')
            found = rule.get('found')

            if selector == "_text":
                result = soup.find(text=pattern)
            else:
                result = soup.findSelect(selector)

            if found != bool(result):
                success = False
                break

        return success

    ### Utility functions
    def normalize_params(self, source_params, criteria):
        if not source_params:
            return criteria

        # Look through all the get / post variables
        for var, val in source_params.iteritems():
            param = self.parameters.get(var)

            # If the variable is on our list to convert...
            if param and param['name'] in source_params.keys():

                # ... then convert to a normalized form
                field = self.format_paramater(param.get('type'), val)
                source_params[param['name']] = field

        return source_params

    def format_parameter(self, type, value):
        conversions = {
            'date': self.format_date
        }

        try:
            return conversions.get(type)(value)
        except TypeError:
            raise ValueError('Unrecognized conversion type')

    def format_date(self, date_str):
        date_format = self.formats.get('date')
        if not date_format:
            return date_str

        original = datetime.strptime(date_str, '%Y-%m-%d')
        formatted = original.strftime(date_format)
        return formatted