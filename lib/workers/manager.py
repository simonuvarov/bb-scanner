from lib.observers import MainObserver
from lib.workers.masscan import MasscanWorker
from lib.workers.nmap import NmapWorker


class Manager:
    def __init__(self):
        self._observer = MainObserver()
        self._nm1 = NmapWorker()
        self._nm2 = NmapWorker()
        self._nm3 = NmapWorker()
        self._ms1 = MasscanWorker()
        self._ms2 = MasscanWorker()
        self._ms3 = MasscanWorker()



    def run(self):
        self._observer.start()
        self._nm1.start()
        self._nm2.start()
        self._nm3.start()

        self._ms1.start()
        self._ms2.start()
        self._ms3.start()