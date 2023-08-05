import socket
import time


def wait_for_port(port, host='localhost', timeout=4):
    start = time.time()

    while True:
        try:
            s = socket.create_connection((host, port), 1)
            s.close()
            return True
        except socket.error:
            pass

        time.sleep(0.1)

        if time.time() - start > timeout:
            return False


def find_free_port(start, stop=32000):
    for port in range(start, stop):
        sock = socket.socket()
        try:
            sock.bind(('', port))
            sock.close()
            return port
        except Exception:
            continue
    return None
