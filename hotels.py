from utils import Hotel, visit_page
from pyquery import PyQuery as pq

class Doubletree(Hotel):
    __keywords = {
        "arrival": "arrivalDate",
        "departure": "departureDate"
    }    
    __pages = [{
        "url": "https://secure3.hilton.com/en_US/dt/reservation/book.htm",
        "data": {
            "ctyhocn": "YYZIPDT"                #UNKNOWN: City Hotel Code?
        }
    }, {
        "url": "https://secure3.hilton.com/en_US/dt/reservation/book.htm?execution=e1s1",
        "data": {
            "arrivalDate": "25 May 2012",
            "departureDate": "27 May 2012",
            "_flexibleDates": "on",
            "_rewardBooking": "on",
            "numberOfRooms": "1",
            "numberOfAdults[0]": "4",
            "numberOfChildren[0]": "0",
            "numberOfAdults[1]": "1",
            "numberOfChildren[1]": "0",
            "numberOfAdults[2]": "1",
            "numberOfChildren[2]": "0",
            "numberOfAdults[3]": "1",
            "numberOfChildren[3]": "0",
            "promoCode": "",
            "srpId": "",
            "onlineValueRate": "",
            "groupCode": "AME",
            "corporateId": "",
            "_rememberCorporateId": "on",
            "_aaaRate": "on",
            "_aarpRate": "on",
            "_governmentRate": "on",
            "_travelAgentRate": "on",
            "_eventId_findRoom": "Continue",
            "execution": "e5s2"
        }
    }]
    
    
    def __init__(self, opener):
        self.__opener = opener
    
    def check_availability(self, **kwargs):
        response = ""
        for page in self.__pages:
            response = visit_page(self.__opener, page["url"], self.patch_data(page["data"], **kwargs)) #Is it not possible to use dot notation with python dictionaries?
        self.analyze_response(response)
        
    def patch_data(self, data, **kwargs):
        #TODO: run hotel specific function on value
        
        #A bit messy, but convert generic args to hotel specific
        for key, value in kwargs.items():
            if key in self.__keywords.keys():
                data[self.__keywords[key]] = value
        return data
        
    def analyze_response(self, html):
        query = pq(html)
        if query("#roomViewRegularView"):
            print("At least one room is available!")
        else:
            print("No rooms are available")
        
