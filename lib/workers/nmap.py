import json

import beanstalkc
from loguru import logger
from nmap import PortScanner

from lib.storage.database import Database
from lib.storage.models import SinglePort, SingleHost
from lib.utils import is_valid_ipv4_address, timestamp
from lib.workers.base_worker import BaseWorker


class NmapWorker(BaseWorker):
    def scan(self, host: str, ports, arguments: str = "-T4 -PN -n -sV") -> SingleHost:
        """

        :type ports: int
        """
        if not is_valid_ipv4_address(host):
            return None

        # in case we forgot to case port to str
        if ports is int:
            ports = str(ports)

        # TODO: get timestamp from the scan result
        t = timestamp()
        nm = PortScanner()
        nm.scan(host, str(ports), arguments=arguments)

        # TODO: add support of UDP ports
        ports = nm[host]['tcp']

        # We want to return the whole host structure

        result = SingleHost(host, t)
        for key in ports:
            new_port = SinglePort(cpe=ports[key]['cpe'], port=str(key), state=ports[key]['state'],
                                  name=ports[key]['name'], reason=ports[key]['reason'], timestamp=t)
            result.new_port(new_port)
        return result

    def parse_xml(self):
        # TODO: add
        pass

    def parse_grep(self):
        # TODO: add
        pass

    def __f(self, job):
        logger.debug("NmapWorker has taken a job for {}", job)
        job_json = json.loads(job)
        host = job_json['host']
        port = job_json['port']
        db = Database()
        result = self.scan(host, port)
        db.update_host(result)
        db.close_connection()

    def run(self):
        logger.debug('NmapWorker has started')
        beanstalk = beanstalkc.Connection(host='localhost', port=11300)
        beanstalk.watch('nmap')
        beanstalk.ignore('default')
        while True:
                job = beanstalk.reserve()
                self.__f(job.body)
                job.delete()


