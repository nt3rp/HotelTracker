import unittest
from hoteltracker.utils import list_missing_args

class TestUtils(unittest.TestCase):
    def setUp(self):
        pass

    def test_list_required_arguments_no_args(self):
        expected = set()
        actual = list_missing_args()
        self.assertEqual(expected, actual)

    def test_list_required_arguments_missing_provided(self):
        expected = set(('a', 'b', 'c'))
        actual = list_missing_args(('a','b','c'))
        self.assertEqual(expected, actual)

    def test_list_required_arguments_missing_required(self):
        expected = set()
        actual = list_missing_args(provided=('a','b','c'))
        self.assertEqual(expected, actual)

    def test_list_required_arguments(self):
        expected = set('c')
        actual = list_missing_args(required=('a','b','c'), provided=('a','b'))
        self.assertEqual(expected, actual)

    def test_list_required_argument_with_message(self):
        expected = "Missing argument: c"
        actual = list_missing_args(required=('a','b','c'),
            provided=('a','b'),
            message='Missing argument{s}: {args}')
        self.assertEqual(expected, actual)

    def test_list_required_argument_with_plural_message(self):
        expected = "Missing arguments: a, c"
        actual = list_missing_args(required=('a','b','c'),
            provided='b',
            message='Missing argument{s}: {args}')
        self.assertEqual(expected, actual)

