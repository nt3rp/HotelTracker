import argparse
import logging
import sys
from hoteltracker.hotels import Doubletree
from hoteltracker.utils import TwitterHandler

def main():
    logger = logging.getLogger('hotel_tracker')
    logger.setLevel(logging.DEBUG)

    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(log_format)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    twitter_handler = TwitterHandler()
    logger.addHandler(twitter_handler)

    parser = argparse.ArgumentParser(description='Try to find out if there is vacancy at a hotel.');
    parser.add_argument(
        '--arrival',
        required=True,
        help='The day you will be arriving.')
    parser.add_argument(
        '--departure',
        required=True,
        help='The day you will be departing.')

    args, unknown = parser.parse_known_args()
    args = vars(args)

    hotel = Doubletree()

    hotel.is_available(**args)


if __name__ == '__main__':
    sys.exit(main())