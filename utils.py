import json
import urllib
import urllib2
import cookielib
from datetime import datetime
from pyquery import PyQuery as pq

def write_file(content, filename = "output.html"):
    open_file = open(filename, 'w')
    open_file.write(content)
    open_file.close()

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

def get_hotels_from_config(opener, filename = "hotels.json"):
    hotels   = []
    config   = open(filename, 'r')
    contents = config.read()
    config.close()
    
    json_obj = json.loads(contents)
    for item in json_obj:
        hotel = create_hotel_from_config(opener, item)
        hotels.append(hotel)
        
    return hotels
    
def create_hotel_from_config(opener, config):
    return HotelWebsite(opener, **config)
    
class HotelWebsite(object):
    def __init__(self, opener, availability_selector = "", params = "", date_format = "", pages = []):
        self.__opener = opener
        self.__param_fns = {
            "arrival": self.__format_date,
            "departure": self.__format_date
        }
        
        self._availability_selector = availability_selector
        self._params = params
        self._date_format = date_format
        self._pages = pages
        
        
    def __patch_data(self, data, **kwargs):
        for key, value in kwargs.items():
            mapped_value = self._params.get(key)
            if mapped_value and mapped_value in data.keys():
                data[self._params[key]] = self.__param_fns[key](value)
        return data
    
    def __format_date(self, str_date):
        original_date = datetime.strptime(str_date, "%Y-%m-%d")
        formatted_date = original_date.strftime(self._date_format)
        return formatted_date
        
    def __analyze_response(self, html):
        query = pq(html)
        if query(self._availability_selector):
            print("At least one room is available!")
        else:
            print("No rooms are available")
    
    def check_availability(self, **kwargs):
        response = ""
        for page in self._pages:
            url = page["url"]
            data = self.__patch_data(page["data"], **kwargs)
            response = visit_page(self.__opener, url, data)
        self.__analyze_response(response)
