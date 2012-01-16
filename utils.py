import urllib
import urllib2
import cookielib

def create_url_opener(cookie_jar = None):
    if cookie_jar is None:
        cookie_jar = cookielib.CookieJar()

    url_opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar))
    return url_opener

def visit_page(url_opener, url, data={}):
    if type(data) is dict:
        data = urllib.urlencode(data)

    #TODO: handle open errors
    response = url_opener.open(url, data)
    results  = response.read()
    response.close()
    return results
    
class Hotel(object):
    def check_availability(self, **kwargs):
        """Checks the availability of the hotel using available requirements"""
        raise NotImplementedError( "Should have implemented this" )
