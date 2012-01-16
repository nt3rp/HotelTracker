#!/usr/bin/python2
import sys
from utils import create_url_opener, visit_page
from hotels import Doubletree

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
    opener = create_url_opener()
    hotel = Doubletree(opener)
    hotel.check_availability()

if __name__ == "__main__":
    sys.exit(main())
