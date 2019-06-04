import unittest

from lib import utils


class BasicTest(unittest.TestCase):
    def test_is_valid_ipv4_address_valid_ip(self):
        result = utils.is_valid_ipv4_address('1.1.1.1')
        self.assertTrue(result, "Must be True")

    def test_is_valid_ipv4_address_wrong_ip(self):
        result = utils.is_valid_ipv4_address('256.1.1.1')
        self.assertFalse(result, "Must be False")

        result = utils.is_valid_ipv4_address('google.com')
        self.assertFalse(result, "Must be False")

        result = utils.is_valid_ipv4_address('8.8.8.0/24')
        self.assertFalse(result, "Must be False")

if __name__ == '__main__':
    unittest.main()