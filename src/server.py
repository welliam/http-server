# -*- coding: utf-8 -*-

import socket
import string
import utils


class HTTPException(Exception):
    pass


def format_response(status_line, headers, content):
    """Building HTTP protocol-compliant response."""
    return u'{}\r\n{}\r\n\r\n{}\r\n'.format(
        status_line,
        format_headers(headers),
        content
    )


def format_headers(headers):
    """Builds headers as a string from headers dict."""
    return u'\r\n'.join('{}: {}'.format(k, headers[k]) for k in headers)


def response_ok():
    """Returns formatted 200 response"""
    status_line = u'HTTP/1.1 200 OK'
    headers = {u'Content-Type': 'text/html; charset=UTF-8'}
    content = u'<h1>Hello world!</h1>'
    return format_response(status_line, headers, content)


def response_error():
    """Returns formatted 500 response"""
    status_line = u'HTTP/1.1 500 Internal Server Error'
    headers = {u'Content-Type': 'text/html; charset=UTF-8'}
    content = u'Internal server error.'
    return format_response(status_line, headers, content)


def split_head(request):
    splitted = request.split('\r\n\r\n', 1)
    return splitted[0], '' if len(splitted) == 1 else splitted


def combine_continued_headers(headers):
    result = []
    for line in headers:
        if line and line[0] in string.whitespace:
            try:
                result[-1] += line.lstrip()
            except IndexError:
                raise HTTPException('First header line started with whitespace.')
        else:
            result.append(line)
    return result


def parse_headers(header_lines):
    headers = combine_continued_headers(header_lines)
    try:
        return {
            key.lower(): value for key, value in
            map(lambda s: s.split(':', 1), headers)
        }
    except ValueError:
        raise HTTPException('Header line has no colon')


def verify_head(method, http_version, headers):
    if method != 'GET':
        raise HTTPException('Method is not GET')
    if http_version != 'HTTP/1.1':
        raise HTTPException('HTTP version is not 1.1')
    if 'host' not in headers:
        raise HTTPException('Host not in header')


def parse_request(request):
    head, body = split_head(request)
    head_lines = list(filter(lambda x: x, head.split('\r\n')))
    try:
        status_line = head_lines[0]
    except IndexError:
        raise HTTPException('Request is empty')
    headers = parse_headers(head_lines[1:])
    try:
        method, uri, http_version = status_line.split()
    except ValueError:
        raise HTTPException('Invalid status line')
    verify_head(method, http_version, headers)
    return uri


def start_server():
    """Set up server socket."""
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
    """Set up client socket"""
    while True:
        conn, addr = server_socket.accept()
        message = utils.recieve_message(conn)
        print(message)
        conn.sendall(response_ok().encode('utf8'))
        conn.close()


if __name__ == '__main__':
    server_socket = start_server()
    try:
        server(server_socket)
    except KeyboardInterrupt:
        server_socket.close()
