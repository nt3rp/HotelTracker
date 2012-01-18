#!/usr/bin/python2
import sys
import argparse
from utils import create_url_opener, visit_page, get_hotels_from_config
from hotels import Doubletree
import cookielib
import time
from datetime import datetime

class LazyMessager(object):
    def __init__(self):
        self.__first_run         = True
        self.__last_message      = ""
        self.__last_availability = False
        self.__last_change       = datetime.now()
        
    def _update(self, result):
        self.__last_message      = result["message"]
        self.__last_availability = result["availability"]
        self.__last_change       = datetime.now()
        
    def has_changed(self, result):
        time_delta = datetime.now() - self.__last_change;
        time_delta_in_hours = time_delta.seconds / 3600
        return (self.__first_run or
            self.__last_message      != result["message"] or
            self.__last_availability == result["availability"] or
            time_delta_in_hours > 24);
        
    def message(self, result):
        if self.has_changed(result):
            self.__first_run = False
            self._update(result)
            print(self.__last_message)

def main():
    #Parse arguments
    parser = argparse.ArgumentParser(description='Try to find hotel availability');
    parser.add_argument('--arrival', required=True, help="The day you will be arriving")
    parser.add_argument('--departure', required=True, help="The day you will be departing")
    parser.add_argument('--frequency', type=float, default=5, help="How often (in minutes) to check for hotel availability. Defaults to every 5 minutes.")
    parser.add_argument('--config', default="hotels.json", help="Config file to use. Defaults to 'hotels.json'")
    
    #Convert from namespace to dictionary
    arguments = vars(parser.parse_args());

    cookie_jar = cookielib.CookieJar()
    opener = create_url_opener(cookie_jar)
    hotels = get_hotels_from_config(opener, arguments["config"])
    
    message_log = {}
    
    for hotel in hotels:
        hotel_name = hotel.get_display_name()
        message_log[hotel_name] = LazyMessager()
    
    if arguments["frequency"] == 0:
        for hotel in hotels:
            result = hotel.check_availability(**arguments)
            hotel_name = hotel.get_display_name();
            message_log[hotel_name].message(result)
    else:
        while True:
            try:
                for hotel in hotels:
                    result = hotel.check_availability(**arguments)
                    hotel_name = hotel.get_display_name();
                    message_log[hotel_name].message(result)
                cookie_jar.clear()
                time.sleep(arguments["frequency"] * 60)
            except KeyboardInterrupt:
                print "KeyboardInterrupt received. Halting..."
                break
            except Exception as ex:
                print ex
                break

if __name__ == "__main__":
    sys.exit(main())
