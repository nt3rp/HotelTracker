import argparse
import logging
import sys
import time
from urllib2 import URLError
from twitter import TwitterError
from hoteltracker.hotels import DoubletreeInternationalPlaza, HolidayInn, HolidayInnAirportEast, HolidayInnTorontoInternational
from hoteltracker.utils import TwitterHotelMessager

def main():
    logger = logging.getLogger('hotel_tracker')
    logger.setLevel(logging.INFO)

    log_format = '[%(asctime)s] {%(module)s.py:%(funcName)s:%(lineno)d} ' \
                 '%(levelname)s %(name)s - %(message)s'
    formatter = logging.Formatter(log_format,'%Y-%m-%d %H:%M:%S')

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

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
        required=False,
        help='Path to Twitter JSON.')
    parser.add_argument(
        '--frequency',
        type=float,
        default=5,
        help='How often (in minutes) to check for hotel availability. Defaults to every 5 minutes.')

    args, unknown = parser.parse_known_args()
    args = vars(args)

    handlers = []

    if args.get('twitter_config'):
        twitter_handler = TwitterHotelMessager(
            config_path=args.get('twitter_config')
        )
        handlers.append(twitter_handler)


    hotels = [
        DoubletreeInternationalPlaza(),
        HolidayInnAirportEast(),
        HolidayInnTorontoInternational()
    ]

    frequency = args.get('frequency')
    while True:
        try:
            for hotel in hotels:
                available = hotel.is_available(**args)
                logger.info('{0}: Available? {1}'.format(hotel._name, available))

                for handler in handlers:
                    handler.update(hotel._name, available)

            if frequency == 0:
                break

            time.sleep(frequency * 60)
        except KeyboardInterrupt:
            print '\nKeyboardInterrupt received. Halting...'
            break
        except (URLError, TwitterError), e:
            logger.error(e)
        except Exception, e2:
            logger.error('Unexpected Error: {0}'.format(e2))


if __name__ == '__main__':
    sys.exit(main())
