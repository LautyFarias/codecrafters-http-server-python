import socket

ACCEPTED_BUFFSIZE = 1024
"""Accepted request buffer size by the socket server."""

ROOT_PATH = "/"
"""Represents the root path of the server."""


def main() -> None:
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    connection, _client_address = server_socket.accept()  # wait for client

    buffer = connection.recv(ACCEPTED_BUFFSIZE)

    _method, path, *_rest = buffer.decode().split()

    if path == ROOT_PATH:
        response = b"HTTP/1.1 200 OK\r\n\r\n"
    else:
        response = b"HTTP/1.1 404 OK\r\n\r\n"

    connection.send(response)


if __name__ == "__main__":
    main()
