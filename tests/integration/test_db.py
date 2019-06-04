import unittest

from lib.storage.database import Database
from lib.workers.amass import Amass
from lib.workers.masscan import Masscan


class FullFlow(unittest.TestCase):
    def setUp(self):
        self.database = Database(database_name='test')
        self.amass = Amass()
        self.amass_hosts = self.amass.parse_output_file('test_data/amass.json')
        self.masscan = Masscan()
        self.masscan_hosts = self.masscan.parse_json_output('test_data/masscan.json')

    def test_inserting_hosts(self):
        self.database.update_hosts(self.amass_hosts)
        self.database.delete_host('1.1.1.1')
        self.database.update_hosts(self.amass_hosts)
        # TODO: asserts here

    def test_masscan(self):
        self.database.update_hosts(self.amass_hosts)
        self.database.update_hosts(self.masscan_hosts)
'''
    def test_insert_document(self):
        self.database.flush_all_tables()

        # Send subdomains and hosts
        self.database.update_hosts(self.hosts)
        hosts = list(self.database.get_hosts())
        self.assertEqual(len(hosts), len(self.ips), "Wrong number of hosts")

    def test_send_masscan_results(self):
        self.database.flush_all_tables()
        self.database.insert_host_document(self.ips)
        # Send masscan results
        self.database.update_host(self.hosts)

        # Check the structure of JSON for a host
        host = self.database.get_host('1.1.1.1')
        self.assertIsInstance(host, dict, "Must be a dictionary")
        self.assertEqual(host['ip'], '1.1.1.1', "Wrong IP, must 1.1.1.1")
        self.assertEqual(host['ports']['443']['state'], "open", "Wrong status, must be open")
        self.assertEqual(host['ports']['443']['reason'], "syn-ack", "Wrong reason, must be syn-ack")

        # TODO: add "mocked" nmap results

    def test_send_nmap_results(self):
        self.database.flush_all_tables()
        self.database.insert_host_document(self.ips)
        # Send masscan results
        self.database.update_host(self.hosts)
        scan_result = {'443':{
            "cpe": "",
            "name": "https",
            "reason": "syn-ack",
            "state": "open",
            "timestamp": 1559140073
        }}
        self.database.send_nmap_result('1.1.1.1', scan_result)

    def test_send_directories(self):
        self.database.flush_all_tables()
        self.database.insert_host_document(self.ips)
        # Send masscan results
        self.database.update_host(self.hosts)
        scan_result = { '443': {
            "cpe": "",
            "name": "https",
            "reason": "syn-ack",
            "state": "open",
            "timestamp": 1559140073
        }}
        self.database.send_nmap_result('1.1.1.1', scan_result)
        dirs = ['/', '/robots.txt']
        self.database.send_subdirs('1.1.1.1', 443, dirs)
'''

if __name__ == '__main__':
    unittest.main()
