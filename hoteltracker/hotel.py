# -*- coding: utf-8 -*-
import contextlib
import cookielib
import re
import urllib
import urllib2
from bs4 import BeautifulSoup
import soupselect
from datetime import datetime

soupselect.monkeypatch()

# TODO: Create a 'page' interface / class?
# ... could just be a named tuple

# TODO: default to 'tonight' for checkin?

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
                post = self.normalize_params(post, criteria)

            url = page.get('url')
            html = self.visit(url, get, post)

        is_available = self.analyze_response(html)
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

            # TODO: Do not compile this pattern every time
            pattern = re.compile(rule.get('pattern'))
            found = rule.get('found')
            selector = rule.get('selector')

            if selector == "_text":
                result = soup.find(text=pattern)
            else:
                #TODO: Actually use the pattern in this case
                result = soup.findSelect(selector)

            if found != bool(result):
                success = False
                break

        return success

    ### Utility functions
    def normalize_params(self, source_params, criteria):
        if not source_params:
            return criteria

        # Look through all the criteria
        for var, val in criteria.iteritems():
            param = self.parameters.get(var)

            # If the criteria is on our list to convert...
            if param and param['name'] in source_params.keys():

                # ... then convert to a normalized form
                field = self.format_parameter(param.get('type'), val)
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