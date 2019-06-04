import rethinkdb as rdb
from loguru import logger

# TODO: add check that the database exists and its tables exist. If not, then create
class Database:
    def __init__(self, host='localhost', port=28015, database_name='octopus'):
        self._db_name = database_name
        self._host = host
        self._port = port

        self._r = rdb.RethinkDB()
        self._connection = self._r.connect(host, port)

        self._connection.use(self._db_name)

    def close_connection(self):
        self._connection.close()

    def __flush_table(self, table_name):
        result = self._r.db(self._db_name).table(table_name).delete().run(self._connection)
        return result

    def flush_all_tables(self):
        """
        Deletes all entries from all tables
        """
        self.__flush_table('hosts')

    def get_hosts(self):
        """
        Returns all hosts from the database
        :return:
        """
        cursor = self._r.db(self._db_name).table('hosts').run(self._connection)
        return cursor

    def get_host(self, ip):
        """
        Return host entry by its IP address
        :param ip:
        :return:
        """
        result = self._r.db(self._db_name).table("hosts").get(ip).run(self._connection)
        return result

    def get_hosts_port(self, target_port: int) -> object:
        """
        Returns hosts containing the open port
        :param target_port:
        :return:
        """
        result = self._r.db(self._db_name).table('hosts').filter({'ports': {str(target_port): {'state': 'open'}}}).run(
            self._connection)
        return result

    def insert_hosts(self, hosts: list):
        """
        Inserts information about hosts
        :param hosts:
        """
        result = self._r.db(self._db_name).table('hosts').insert(hosts.to_json()).run(self._connection)

    def update_hosts(self, hosts: list):
        """
        Updates information about hosts
        :param hosts:
        """
        for host in hosts:
            self.update_host(host)

    def update_host(self, host: object):
        """
        Updates information about a single host
        :param host:
        """
        host_in_json = host.to_json()
        result = None
        if not self.get_host(host.ip):
            result = self._r.db(self._db_name).table('hosts').insert(host_in_json).run(self._connection)
        result = self._r.db(self._db_name).table('hosts').get(host.ip).update(host_in_json).run(self._connection)

    def update_ports(self, target_host, ports: dict):
        """
        Updates information about ports for a single host
        :param target_host:
        :param ports:
        :return:
        """
        logger.debug("Adding port info for {}", target_host)
        result = self._r.table('hosts').get(target_host).update({'ports': ports}).run(self._connection)
        return result

    def delete_host(self, target_host: str):
        result = self._r.table('hosts').get(target_host).delete().run(self._connection)
        logger.debug(result)

    def get_hosts_by_subdomain(self, pattern):
        result = self._r.db(self._db_name).table('hosts').filter(
            lambda host: host['subdomains'].contains(lambda s: s.match(pattern))).run(self._connection)
        return result

    def get_hosts_no_nmap(self):
        result = self._r.db(self._db_name).table('hosts').filter(
            lambda host: host['ports'].contains(lambda p: p.has_fields('name') == False)).run(self._connection)
        return result

    def subscribe_to_new_ports(self):
        cursor = self._r.db(self._db_name).table('hosts').changes().filter(
            lambda change: change['new_val']['ports'].contains(lambda p: p.has_fields('name') == False)).run(
            self._connection)
        return cursor

    def subscribe_to_new_hosts(self):
        cursor = self._r.db(self._db_name).table('hosts').changes().filter(
            lambda change: change['old_val'] == None).run(
            self._connection)
        return cursor

    def get_hosts_with_no_screenshot(self):
        result = self._r.db(self._db_name).table('hosts').filter(
            lambda host: host['ports'].contains(lambda p: p.has_fields('screenshot') == False)).run(self._connection)

