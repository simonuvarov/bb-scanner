import json
from multiprocessing import Process

import beanstalkc
from loguru import logger

from lib.storage.database import Database


class BaseObserver(Process):
    pass


class HostObserver(BaseObserver):
    def run(self):
        db = Database()
        cursor = db.subscribe_to_new_hosts()

        beanstalk = beanstalkc.Connection(host='localhost', port=11300)
        beanstalk.use('masscan')
        for item in cursor:
            host = item['new_val']
            # TODO: check if port has already been scanned, we can skip it when getting info, but...
            beanstalk.put(json.dumps({"host": host['ip']}))
            #logger.debug("Found a new host {}", host['ip'])


class PortObserver(BaseObserver):
    def run(self):
        db = Database()
        cursor = db.subscribe_to_new_ports()

        beanstalk = beanstalkc.Connection(host='localhost', port=11300)
        beanstalk.use('nmap')
        for item in cursor:
            host = item['new_val']
            # TODO: check if port has already been scanned, we can skip it when getting info, but...
            for port in host['ports']:
                beanstalk.put(json.dumps({"host": host['ip'], "port": port['port']}))
                logger.debug("Found a new port {}:{}", host['ip'], port['port'])


class MainObserver(Process):
    def run(self):
        logger.debug("Watchdog has started")
        p1 = PortObserver()
        p1.start()

        p2 = HostObserver()
        p2.start()