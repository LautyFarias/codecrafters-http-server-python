import enum
import socket

ACCEPTED_BUFFSIZE = 1024
"""Accepted request buffer size by the socket server."""


class Route(enum.StrEnum):
    """
    Enumeration of available routes.
    """

    ROOT = "/"
    ECHO = "/echo/"


def main() -> None:
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    connection, _client_address = server_socket.accept()  # wait for client

    buffer = connection.recv(ACCEPTED_BUFFSIZE)

    _method, path, *_rest = buffer.decode().split()

    if path == Route.ROOT:
        response = "HTTP/1.1 200 OK\r\n\r\n"

    elif path.startswith(Route.ECHO):
        random_string = path.replace(Route.ECHO, "", 1)
        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/plain\r\n"
            f"Content-Length: {len(random_string)}\r\n\r\n"
            f"{random_string}"
        )

    else:
        response = "HTTP/1.1 404 OK\r\n\r\n"

    connection.send(response.encode())


if __name__ == "__main__":
    main()
