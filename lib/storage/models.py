class SinglePort():
    def __init__(self, port, timestamp, cpe=None, name=None, reason=None, state=None, source=None, screenshot=None):
        self.cpe = cpe
        self.port = int(port)
        self.name = name
        self.reason = reason
        self.state = state
        self.timestamp = timestamp
        self.source = source
        self.screenshot = screenshot

    @property
    def number(self):
        return self.port

    def to_json(self):
        # It only returns fields that exist. Thus, we don't have to update part of the table
        # and can push the whole object. Otherwise, it would replace existing fields with emptiness
        result = {}
        if self.cpe is not None:
            result['cpe'] = self.cpe
        if self.name is not None:
            result['name'] = self.name
        if self.reason is not None:
            result['reason'] = self.reason
        if self.state is not None:
            result['state'] = self.state
        if self.source is not None:
            result['source'] = self.source
        if self.screenshot is not None:
            result['screenshot'] = self.screenshot

        result['port'] = self.port
        result['timestamp'] = self.timestamp
        return result


class SingleHost():
    def __init__(self, ip, timestamp, asn=None, cidr=None, desc=None, ports=None, subdomains=None):
        self.asn = asn
        self.cidr = cidr
        self.desc = desc
        self.ip_addr = ip
        self.ports = ports
        self.subdomains = subdomains
        self.timestamp = timestamp

    @property
    def ip(self):
        return self.ip_addr

    def subdomain_exists(self, subdomain):
        for sub in self.subdomains:
            if sub == subdomain:
                return True
        return False

    def port_exists(self, port: int):
        if self.ports is None:
            return False

        for p in self.ports:
            if p.number == port:
                return True

        return False

    def new_subdomain(self, subdomain: str):
        if self.subdomain_exists(subdomain):
            pass  # TODO
        self.subdomains.append(subdomain)

    def new_port(self, port):
        if self.port_exists(port.number):
            pass
        if self.ports is None:
            self.ports = []
        self.ports.append(port)

    def new_screenshot(self, port):
        pass  # TODO

    def to_json(self):
        result = {}
        if self.asn is not None:
            result['asn'] = self.asn
        if self.cidr is not None:
            result['cidr'] = self.cidr
        if self.desc is not None:
            result['desc'] = self.desc
        if self.ports is not None:
            result['ports'] = []
            for port in self.ports:
                result['ports'].append(port.to_json())
        if self.subdomains is not None:
            result['subdomains'] = self.subdomains

        result['ip'] = self.ip_addr
        result['timestamp'] = self.timestamp

        return result


class HostList:
    def __init__(self, hosts=None):
        if hosts is None:
            self.hosts = []
        else:
            self.hosts = hosts

    def __iter__(self):
        return iter(self.hosts)

    def new_host(self, host: object):
        if self.host_exists(host.ip):
            pass
        self.hosts.append(host)

    def host_exists(self, ip: str):
        for host in self.hosts:
            if host.ip == ip:
                return True
        return False

    def get_host(self, ip: str):
        for host in self.hosts:
            if host.ip == ip:
                return host
        return None

    def to_json(self):
        result = []
        for host in self.hosts:
            result.append(host.to_json())
        return result
