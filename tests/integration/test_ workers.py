import unittest

from lib.workers import nmap
from lib.workers import screenshotter
from lib.workers.amass import Amass


class BasicTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_parse_amass_file(self):
        amass = Amass()
        hosts = amass.parse_output_file('test_data/amass.json')
        self.assertEqual(len(hosts), 2, "Must be 2 IPs")
        self.assertIsInstance(hosts, list, "Must be a list")

    def test_nmap_scan(self):
        result = nmap.scan_single_host('1.1.1.1', '443')
        self.assertEqual(len(result), 1, "Must be 1 result")

        result = nmap.scan_single_host('1.1.1.1, 8.8.8.8', '443')
        self.assertFalse(result, "Must not have run scan")

    def test_screenshotter(self):
        screenshotter.take_screenshot("http://google.com")
        # TODO: add assertion here

    def test_locate_chrome(self):
        result = screenshotter.locate_chrome()
        self.assertNotEqual(result, "", "Must have return path to Chrome")


if __name__ == '__main__':
    unittest.main()
