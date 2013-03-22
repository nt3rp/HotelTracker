import argparse
import sys
from hoteltracker.hotels import Doubletree

def main():
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