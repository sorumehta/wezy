from typing import Tuple


class Request:
    def __init__(self, http_method, resource, headers=None, parameters=None, socket_of=None):
        self.http_method = http_method
        self.resource = resource
        self.headers = headers
        self.parameters = parameters
        self.socket_of = socket_of


def parse_request(text: str) -> Tuple[Request, int]:
    request_line = text.splitlines()[0]
    request_line = request_line.rstrip('\r\n')
    request_method, path, http_version = request_line.split()
    assert (http_version == "HTTP/1.1")
    request = Request(http_method=request_method, resource=path)
    expecting = 0
    return request, expecting
