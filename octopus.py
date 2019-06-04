from lib.storage.database import Database
from lib.workers.amass import Amass
from lib.workers.manager import Manager

if __name__ == '__main__':
    manager = Manager()
    manager.run()
    db = Database()
    db.flush_all_tables()
    amass = Amass()
    hosts = amass.parse_output_file('C:\\Users\\seuv\\Desktop\\amass.json')
    db.insert_hosts(hosts)
