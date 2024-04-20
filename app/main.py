import enum
import socket
from threading import Thread

ACCEPTED_BUFFSIZE = 1024
"""Accepted request buffer size by the socket server."""


class Route(enum.StrEnum):
    """
    Enumeration of available routes.
    """

    ROOT = "/"
    USER_AGENT = "/user-agent"
    ECHO = "/echo/"


class Status(enum.StrEnum):
    OK = "200 OK"
    NOT_FOUND = "404 Not Found"


class Response:
    version = "HTTP/1.1"
    content_type = "text/plain"

    def __init__(self, status: Status = Status.OK, data: str = "") -> None:
        self.status = status

        self.data = data
        self.content_length = len(data)

    def __bytes__(self) -> bytes:
        response = f"{self.version} {self.status}\r\n"

        if self.data:
            response += (
                f"Content-Type: {self.content_type}\r\n"
                f"Content-Length: {self.content_length}\r\n\r\n"
                f"{self.data}"
            )
        else:
            response += "\r\n\r\n"

        return response.encode()


def handle_connection(connection: socket.socket) -> None:
    with connection:
        buffer = connection.recv(ACCEPTED_BUFFSIZE)

        metadata, *headers = buffer.decode().split("\r\n")
        _method, path, _version = metadata.split()

        if path == Route.ROOT:
            response = Response()

        elif path.startswith(Route.ECHO):
            random_string = path.replace(Route.ECHO, "", 1)
            response = Response(data=random_string)

        elif path.startswith(Route.USER_AGENT):
            user_agent_header = next(
                header for header in headers if "User-Agent" in header
            )

            _header, user_agent = user_agent_header.split(":")

            response = Response(data=user_agent.strip())

        else:
            response = Response(Status.NOT_FOUND)

        connection.send(bytes(response))


def main() -> None:
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    while True:
        connection, _client_address = server_socket.accept()  # wait for client

        thread = Thread(target=handle_connection, args=(connection,))
        thread.start()


if __name__ == "__main__":
    main()
