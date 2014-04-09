import unittest
from hoteltracker import HotelWebsite

class HotelWebsiteSetup(unittest.TestCase):
    def setUp(self):
        pass

    def test_constructor_no_args(self):
        self.assertRaises(ValueError, HotelWebsite)

    def test_constructor_missing_pages_argument(self):
        self.assertRaises(ValueError, HotelWebsite, banana='test')

    def test_constructor_page_arg_is_not_iterable(self):
        self.assertRaises(TypeError, HotelWebsite, **{
            'name': '',
            'parameters': '',
            'pages': 1,
            'conditions': []
        })

    def test_constructor_keys_are_protected(self):
        hotel = HotelWebsite(**{
            'name': '',
            'parameters': '',
            'pages': [],
            'conditions': []
        })
        def access_pages():
            x = hotel.pages
        self.assertRaises(AttributeError, access_pages)
        x = hotel._pages # Should not raise an exception

    # TODO: Verify we get arguments we're expecting

class HotelWebsiteFunctions(unittest.TestCase):
    def setUp(self):
        self.hotel = HotelWebsite(**{
            'name': '',
            'parameters': '',
            'pages': [],
            'conditions': []
        })

    def test_is_available_no_args(self):
        self.assertRaises(ValueError, self.hotel.is_available)

    # TODO: Verify we get arguments we're expecting (e.g. dates, or date strings)

# TODO: Make a more 'real' unit test that mocks URL requests, etc.
# TODO: Use Nose? Unittest2?

if __name__ == '__main__':
    unittest.main()