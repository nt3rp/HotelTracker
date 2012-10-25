#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import cookielib
import logging
import sys
import time
from twitter import TwitterError
from models import HotelWebsite, TwitterHotelMessager
from util import create_url_opener, check_hotels

def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description='Try to find out if there is vacancy at a hotel.');
    parser.add_argument(
        '--arrival',
        required=True,
        help='The day you will be arriving.')
    parser.add_argument(
        '--departure',
        required=True,
        help='The day you will be departing.')
    parser.add_argument(
        '--twitter-config',
        default='./data/twitter.json',
        help='Path to Twitter JSON.')
    parser.add_argument(
        '--frequency',
        type=float,
        default=5,
        help='How often (in minutes) to check for hotel availability. Defaults to every 5 minutes.')
    parser.add_argument(
        '--config',
        default='./data/hotels.json',
        help='Path to hotel configuration json.')
    parser.add_argument(
        '--log',
        default='critical',
        help='Set the log level of the application.')

    # Convert from namespace to dictionary
    arguments = vars(parser.parse_args());

    # Set logger
    log_level = getattr(logging, arguments.get('log').upper(), None)
    logging.basicConfig(level=log_level)

    logging.info('main: Creating cookie jar and URL opener')
    cookie_jar = cookielib.CookieJar()
    opener = create_url_opener(cookie_jar)

    logging.info('main: Getting list of hotels')
    hotels = HotelWebsite.from_json_file(opener, arguments['config'])

    logging.info('main: Getting Twitter variables')
    messager = TwitterHotelMessager(arguments['twitter_config'])

    if arguments['frequency'] <= 0:
        check_hotels(hotels, arguments, cookie_jar, messager)
        return

    while True:
        try:
            check_hotels(hotels, arguments, cookie_jar, messager)
            time.sleep(arguments["frequency"] * 60)
        except KeyboardInterrupt:
            print '\nKeyboardInterrupt received. Halting...'
            break
        except TwitterError, e:
            logging.error(e)

if __name__ == '__main__':
    sys.exit(main())