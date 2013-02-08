import unittest
from hoteltracker import HotelWebsite

class TestHotelWebsiteSetup(unittest.TestCase):
    def setUp(self):
        pass

    def test_no_args_constructor(self):
        self.assertRaises(ValueError, HotelWebsite)

    def test_missing_pages_argument_constructor(self):
        self.assertRaises(ValueError, HotelWebsite, banana='test')

    # TODO: Verify we get arguments we're expecting

class TestHotelWebsiteFunctions(unittest.TestCase):
    def setUp(self):
        self.hotel = HotelWebsite(pages=[])

    def test_is_available_no_args(self):
        self.assertRaises(ValueError, self.hotel.is_available)

    def test_is_available_no_arrival(self):
        self.assertRaises(ValueError, self.hotel.is_available,
            departure='banana')

    def test_is_available_no_departure(self):
        self.assertRaises(ValueError, self.hotel.is_available,
            arrival='banana')

    # TODO: Verify we get arguments we're expecting (e.g. dates, or date strings)


if __name__ == '__main__':
    unittest.main()