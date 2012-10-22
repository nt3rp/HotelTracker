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

def visit_page(url_opener, url, data={}, method="POST"):
    if type(data) is dict:
        data = urllib.urlencode(data)

    response = ""
    #TODO: handle open errors
    if method == "POST":
        response = url_opener.open(url, data)
    else:
        url = url + "?" + data
        response = url_opener.open(url)
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
    #TODO: use kwargs?
    def __init__(self, opener, name = "", display = "", availability_selector = "", params = "", date_format = "", pages = []):
        self.__opener = opener
        self.__param_fns = {
            "arrival": self.__format_date,
            "departure": self.__format_date
        }
        
        self._availability_selector = availability_selector
        self._params = params
        self._date_format = date_format
        self._pages = pages
        self._name = name
        self._display = display
        
        
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
        found_element = query(self._availability_selector) #Why does 'query' find something that isn't here?
        
        found = found_element and found_element.html() != self._availability_selector
        message = "{0:s}: "
        if found: 
            message += "At least one room is available!"
        else:
            message += "No rooms are available"
        
        return {
            "availability": found,
            "message": message.format(self._display)
        }
    
    def check_availability(self, **kwargs):
        response = ""
        #counter = 0
        for page in self._pages:
            url = page["url"]
            data = self.__patch_data(page["data"], **kwargs)
            method = page.get("method", "POST")
            response = visit_page(self.__opener, url, data=data, method=method)
            #counter += 1
            #write_file(response, "output" + str(counter) + ".html")
        return self.__analyze_response(response)
        
    def get_name(self):
        return self._name
        
    def get_display_name(self):
        return self._display
