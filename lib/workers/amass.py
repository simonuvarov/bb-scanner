import json

from lib.storage.models import SingleHost, HostList
from lib.utils import is_valid_ipv4_address, read_file_by_line, timestamp


class Amass:

    def __init__(self, path=""):
        self.path = path

    # TODO: rewrite json
    # TODO: run amass from the app
    def parse_output_file(self, path):
        """
        Parses amass output file and return list of hosts
        :param path:
        :return:
        """

        content = read_file_by_line(path)
        return self.parse_output(content)

    def parse_output(self, content):
        hosts = HostList()
        t = timestamp()
        for line in content:
            json_data = json.loads(line)

            ip_addresses = json_data['addresses']
            for ip_address in ip_addresses:
                ip = ip_address['ip']

                # It does not support IPv6 yet
                if not is_valid_ipv4_address(ip):
                    continue

                # Make sure that it's lower cased
                # TODO: check the point sign at the end of the domainname
                subdomain = json_data['name'].lower()

                # if we already have data on this IP
                # the just update its subdomains
                if hosts.host_exists(ip):
                    host = hosts.get_host(ip)
                    host.new_subdomain(subdomain)

                # if it is a new host,
                # then add to the list
                else:
                    host = SingleHost(ip=ip, asn=ip_address['asn'], cidr=ip_address['cidr'], desc=ip_address['desc'],
                                      subdomains=[subdomain], timestamp=t)
                    hosts.new_host(host)
        return hosts

    def run(self):
        output = ""
        return output
