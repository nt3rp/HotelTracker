#!/usr/bin/python2
import sys
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

def write_output(filename, content):
    output_file = open(filename, "w");
    output_file.write(content)
    output_file.close()

def is_hotel_available(html):
    query = pq(html)
    if query("#roomViewRegularView"):
        print("At least one room is available!")
    else:
        print("No rooms are available")

def main():
    doubletree_hotel_url  = "https://secure3.hilton.com/en_US/dt/reservation/book.htm"
    doubletree_hotel_url2 = "https://secure3.hilton.com/en_US/dt/reservation/book.htm?execution=e1s1"

    check_availability_data = {
        "ctyhocn": "YYZIPDT",                                       #UNKNOWN: City Hotel Code?
    }

    check_availability_data2 = {
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

    opener    = create_url_opener()
    #is there a way to avoid visiting this page? Its only purpose seems to be getting the process started
    response  = visit_page(opener, doubletree_hotel_url, check_availability_data)
    write_output("p1.html", response)
    response2 = visit_page(opener, doubletree_hotel_url2, check_availability_data2)
    write_output("p2.html", response2)
    is_hotel_available(response2)

if __name__ == "__main__":
    sys.exit(main())
