import socket
import time


def is_valid_ipv4_address(address):
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:  # no inet_pton here, sorry
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:  # not a valid address
        return False

    return True


def read_file_by_line(path: str) -> list:
    with open(path) as results:
        file_content = results.readlines()
        return file_content


# TODO: convert time to timestamp
def timestamp():
    return int(time.time())
