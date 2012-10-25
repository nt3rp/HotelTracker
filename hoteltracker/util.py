# -*- coding: utf-8 -*-
import cookielib
import urllib2

def create_url_opener(cookie_jar=None):
    if cookie_jar is None:
        cookie_jar = cookielib.CookieJar()

    url_opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar))
    return url_opener

def check_hotels(hotels, arguments, cookie_jar, messager):
    for hotel in hotels:
        available = hotel.is_available(**arguments)
        messager.update(hotel._name, available)

        # Clear all cookies after visiting a hotel
        cookie_jar.clear()