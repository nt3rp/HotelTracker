import cookielib
import urllib2
import time

def create_url_opener(cookie_jar=None):
    if cookie_jar is None:
        cookie_jar = cookielib.CookieJar()

    url_opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar))
    return url_opener

def check_hotels(hotels, arguments, cookie_jar):
    for hotel in hotels:
        hotel.is_available(**arguments)
        time.sleep(arguments["frequency"] * 60)

        # Clear all cookies after visiting a hotel
        cookie_jar.clear()