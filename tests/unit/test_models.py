import unittest

from lib.storage.models import SingleHost, SinglePort, HostList


#import jsonschema

class BasicTest(unittest.TestCase):
    def test_single_port(self):
        port = SinglePort(cpe="cpe_test", port=443, name="https", reason="syn-ack", state="open", timestamp=1234567, source="nmap")
        print(port.to_json())

    def test_single_host(self):
        host = SingleHost(ip='1.1.1.1', asn=12345,cidr='1.1.1.0/24', desc="Description", ports=[], subdomains=[], timestamp=1234567890)
        print(host.to_json())

    def test_host_list(self):
        host1 = SingleHost(ip='1.1.1.1', asn=12345,cidr='1.1.1.0/24', desc="Description", ports=[], subdomains=[], timestamp=1234567890)
        host2 = SingleHost(ip='1.1.1.2', asn=12345,cidr='1.1.1.0/24', desc="Description", ports=[], subdomains=[], timestamp=1234567890)
        hosts = HostList([host1, host2])
        result = hosts.to_json()
        print(result)

if __name__ == '__main__':
    unittest.main()