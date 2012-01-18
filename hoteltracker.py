#!/usr/bin/python2
import sys
import argparse
from utils import create_url_opener, visit_page, get_hotels_from_config
from hotels import Doubletree
import cookielib
import time

def write_output(filename, content):
    output_file = open(filename, "w");
    output_file.write(content)
    output_file.close()

def main():
    parser = argparse.ArgumentParser(description='Try to find hotel availability');
    parser.add_argument('--arrival', required=True, help="The day you will be arriving")
    parser.add_argument('--departure', required=True, help="The day you will be departing")
    parser.add_argument('--frequency', type=float, default=5, help="How often (in minutes) to check for hotel availability. Defaults to every 5 minutes.")
    parser.add_argument('--config', default="hotels.json", help="Config file to use. Defaults to 'hotels.json'")
    
    arguments = vars(parser.parse_args());

    cookie_jar = cookielib.CookieJar()
    opener = create_url_opener(cookie_jar)
    hotels = get_hotels_from_config(opener, arguments["config"])
    
    #TODO: Is this really the best way to determine if we should run this one or more times?
    if arguments["frequency"] == 0:
        for hotel in hotels:
            hotel.check_availability(**arguments)
    else:
        #TODO: is this really the best way to loop?
        while True:
            try:
                for hotel in hotels:
                    hotel.check_availability(**arguments)
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
