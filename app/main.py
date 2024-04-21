import argparse
import enum
from http import HTTPStatus
import socket
from pathlib import Path
from threading import Thread
from typing import Optional

ACCEPTED_BUFFSIZE = 1024
"""Accepted request buffer size by the socket server."""

USER_AGENT_HEADER = "User-Agent"


class Route(enum.StrEnum):
    """
    Enumeration of available routes.
    """

    ROOT = ""
    USER_AGENT = "user-agent"
    ECHO = "echo"
    FILES = "files"


class Response:
    version = "HTTP/1.1"

    def __init__(
        self,
        status: HTTPStatus = HTTPStatus.OK,
        data: str = "",
        content_type: str = "text/plain",
    ) -> None:
        self.status = f"{status} {status.phrase}"
        self.content_type = content_type

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


class NotFoundResponse(Response):
    def __init__(self) -> None:
        super().__init__(HTTPStatus.NOT_FOUND)


def handle_connection(connection: socket.socket, media_directory: Path) -> None:
    with connection:
        buffer = connection.recv(ACCEPTED_BUFFSIZE)

        metadata, *headers = buffer.decode().split("\r\n")
        _method, path, _version = metadata.split()

        path = path.split("/", 2)

        match path[1]:
            case Route.ROOT:
                response = Response()

            case Route.ECHO:
                random_string = path[-1]
                response = Response(data=random_string)

            case Route.USER_AGENT:
                user_agent_header = next(
                    header for header in headers if USER_AGENT_HEADER in header
                )

                _header, user_agent = user_agent_header.split(":")

                response = Response(data=user_agent.strip())

            case Route.FILES:
                filename = path[-1]
                media_path = media_directory / filename

                if not media_path.exists():
                    response = NotFoundResponse()

                else:
                    with open(media_path, "r") as file:
                        response = Response(
                            data=file.read(), content_type="application/octet-stream"
                        )

            case _:
                response = NotFoundResponse()

        connection.send(bytes(response))


def main(media_directory: Optional[Path] = None) -> None:
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    while True:
        connection, _client_address = server_socket.accept()  # wait for client

        thread = Thread(target=handle_connection, args=(connection, media_directory))
        thread.start()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a http server")

    parser.add_argument(
        "--directory",
        metavar="path/to/directory",
        type=Path,
        nargs="?",
        help="The media directory of the server",
    )

    args = parser.parse_args()

    main(args.directory)
