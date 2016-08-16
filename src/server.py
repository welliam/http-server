# -*- coding: utf-8 -*-

import socket
import utils


def build_response(status_line, headers, content):
    return '{}\r\n{}\r\n\r\n{}\r\n'.format(
        status_line,
        '\r\n'.join(headers),
        content
    )


def response_ok():
    status_line = "HTTP/1.1 200 OK"
    headers = ['Content-Type: text/html; charset=UTF-8']
    content = 'Hello world!'
    return build_response(status_line, headers, content)


def response_error():
    status_line = 'HTTP/1.1 500 Internal Server Error'
    headers = ['Content-Type: text/html; charset=UTF-8']
    content = 'Internal server error.'
    return build_response(status_line, headers, content)


def start_server():
    server_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_TCP
    )
    server_socket.bind(utils.address)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.listen(1)
    return server_socket


def server(server_socket):
    while True:
        conn, addr = server_socket.accept()
        message = utils.recieve_message(conn)
        print(message)
        conn.sendall(message)
        conn.close()


if __name__ == '__main__':
    server_socket = start_server()
    try:
        server(server_socket)
    except KeyboardInterrupt:
        server_socket.close()
