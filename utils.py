import urllib
import urllib2
import cookielib
from pyquery import PyQuery as pq

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
    def __init__(self, opener):
        self.__opener = opener
        
        #have to do this here because we don't have a reference to self elsewhere
        self.__keyword_funcs = {
            "arrival": self.format_date,
            "departure": self.format_date
        }
    
    def check_availability(self, **kwargs):
        response = ""
        for page in self._pages:
            response = visit_page(self.__opener, page["url"], self.patch_data(page["data"], **kwargs)) #Is it not possible to use dot notation with python dictionaries?
        self.analyze_response(response)
        
    def patch_data(self, data, **kwargs):
        #TODO: run hotel specific function on value
        
        #A bit messy, but convert generic args to hotel specific
        for key, value in kwargs.items():
            if key in self._keywords.keys():
                data[self._keywords[key]] = self.__keyword_funcs[key](value)
        return data
    
    def format_date(self, str_date):
        return str_date
        
    def analyze_response(self, html):
        query = pq(html)
        if query(self._availability_selector):
            print("At least one room is available!")
        else:
            print("No rooms are available")
    
    
