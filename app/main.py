import socket

ACCEPTED_BUFFSIZE = 1024
"""Accepted request buffer size by the socket server."""

ECHO_PATH = "/echo/"


def main() -> None:
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    connection, _client_address = server_socket.accept()  # wait for client

    buffer = connection.recv(ACCEPTED_BUFFSIZE)

    _method, path, *_rest = buffer.decode().split()

    if path.startswith(ECHO_PATH):
        random_string = path.replace(ECHO_PATH, "", 1)

        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n{random_string}"
    else:
        response = "HTTP/1.1 404 OK\r\n\r\n"

    connection.send(response.encode())


if __name__ == "__main__":
    main()
