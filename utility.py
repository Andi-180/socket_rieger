from socket import socket


def recv(s: socket, n_bytes: int):
    buffer = b''
    while len(buffer) < n_bytes:
        try:
            part = s.recv(n_bytes - len(buffer))
        except BaseException:
            raise ConnectionError(f'could not read from socket {s}')

        if len(part) <= 0:
            raise ConnectionError(f'could not read from socket {s}')
        buffer += part

    return buffer


def send(s: socket, b: bytes):
    n_bytes_sent = 0
    while n_bytes_sent < len(b):
        try:
            sent = s.send(b[n_bytes_sent:])
        except BaseException:
            raise ConnectionError(f'could not write to socket {s}')

        if sent <= 0:
            raise ConnectionError(f'could not write to socket {s}')
        n_bytes_sent += sent