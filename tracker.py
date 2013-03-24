import argparse
import logging
import sys
from hoteltracker.hotels import Doubletree
from hoteltracker.utils import TwitterHotelMessager

def main():
    logger = logging.getLogger('hotel_tracker')
    logger.setLevel(logging.DEBUG)

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

    args, unknown = parser.parse_known_args()
    args = vars(args)

    if True: #args.get('twitter-config'):
        config = args.get('twitter-config', './data/twitter.json')
        twitter_handler = TwitterHotelMessager(
            config_path=config
        )

    hotels = [Doubletree()]

    for hotel in hotels:
        available = hotel.is_available(**args)
        twitter_handler.update(hotel._name, available)


if __name__ == '__main__':
    sys.exit(main())