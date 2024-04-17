import socket


def main() -> None:
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    connection, _client_address = server_socket.accept()  # wait for client
    connection.send("HTTP/1.1 200 OK\r\n\r\n".encode())


if __name__ == "__main__":
    main()
