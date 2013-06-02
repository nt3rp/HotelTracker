import argparse
import logging
import sys
import time
from urllib2 import URLError
from twitter import TwitterError
from hoteltracker.hotels.hilton import DoubletreeInternationalPlaza, \
    HamptonInnSuites, HiltonGardenInnTorontoAirport, HiltonTorontoAirport
from hoteltracker.hotels.holiday_inn import HolidayInnTorontoInternational, \
    HotelIndigoTorontoAirport
from hoteltracker.hotels.marriott import CourtyardTorontoAirport
from hoteltracker.hotels.radisson import Radisson, RadissonTorontoAirport
from hoteltracker.hotels.sheraton import SheratonTorontoAirport
from hoteltracker.utils import TwitterHotelMessager

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
    parser.add_argument(
        '--twitter-config',
        required=False,
        help='Path to Twitter JSON.')
    parser.add_argument(
        '--frequency',
        type=float,
        default=5,
        help='How often (in minutes) to check for hotel availability. Defaults to every 5 minutes.')

    # TODO: add argument for list of hotels, config file

    args, unknown = parser.parse_known_args()
    args = vars(args)

    # TODO: Have group code be a param at 'is_available' time rather than
    # at initialization time

    hotels = [
        # BestWesternPlusTorontoAirport,
        CourtyardTorontoAirport(group_code='aniania'),
        ## CrownePlaza(),
        DoubletreeInternationalPlaza(group_code='ANM'),
        # FairfieldInnAndSuites,
        HamptonInnSuites(group_code='V86'),
        HiltonGardenInnTorontoAirport(group_code='ANI'),
        HiltonTorontoAirport(group_code='ANIM13'),
        ## HolidayInnAirportEast(),
        HolidayInnTorontoInternational(group_code='AEN'),
        ## Hotel Carlingview Toronto Airport - No URL,
        HotelIndigoTorontoAirport(group_code='ANN'),
        ## Marriott(),
        # QualityInnAndSuitesTorontoAirport,
        # QualitySuitesTorontoAirport
        RadissonTorontoAirport(group_code='ANIME'),
        ## ResidenceInn()
        ## Sandman - No URL
        SheratonTorontoAirport(group_code='DEEDE'),
        # WestinBristolPlace,
    ]

    frequency = args.get('frequency')
    while True:
        try:
            for hotel in hotels:
                available = hotel.is_available(**args)

            if frequency == 0:
                break

            time.sleep(frequency * 60)
        except KeyboardInterrupt:
            print '\nKeyboardInterrupt received. Halting...'
            break
        except (URLError, TwitterError), expected_error:
            pass
        except Exception, unexpected_error:
            raise unexpected_error


if __name__ == '__main__':
    sys.exit(main())
