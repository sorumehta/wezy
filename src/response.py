from socket import socket


class Response:
    def __init__(self, content_type="text/html", headers=None, response_code=200, body=None):
        self.content_type = content_type
        self.headers = headers,
        self.response_code = response_code,
        self.body = body if body else ""

    def write_response(self, sock: socket):
        sock.send(self.body)

