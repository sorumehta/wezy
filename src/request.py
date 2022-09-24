from urllib.parse import urlparse, parse_qs
from email.parser import BytesParser


class Request:
    def __init__(self, http_method, resource, headers=None, parameters=None):
        self.http_method = http_method
        self.resource = resource
        self.headers = headers
        self.parameters = parameters


def parse_request(text: str) -> Request:
    request_line, headers_str = text.split('\r\n', 1)
    # request_line = request_line.rstrip('\r\n')
    request_method, path, http_version = request_line.split()
    assert (http_version == "HTTP/1.1")
    parsed_url = urlparse(path)
    headers = dict(BytesParser().parsebytes(headers_str.encode()))
    request = Request(http_method=request_method, resource=parsed_url.path, parameters=parse_qs(parsed_url.query), headers=headers)
    return request
