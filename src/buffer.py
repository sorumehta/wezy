import time
from typing import Tuple

from utils import is_line_terminated
from request import Request
from constants import MAX_REQUEST_SIZE

class Buffer:
    def __init__(self, stream_data):
        self.n_tries = 0
        self.contents = None
        self.stream_data = stream_data
        self.total_buffered = 0
        self.start_time = time.time()
        self.request = None
        self.expecting = 0


    def process_buffer(self):
        self.n_tries += 1
        self.contents = ""
        if not self.stream_data:
            return "EOF!"
        for char in self.stream_data:
            self.contents = char + self.contents
            self.total_buffered += 1
            if self.request:
                self.expecting -= 1
            if is_line_terminated(self.contents):
                parsed, expected = self.parse_request(self.contents[::-1])
                self.request = parsed
                self.expecting = expected
                self.contents = None
                return char
            if self.total_buffered > MAX_REQUEST_SIZE:
                return char

    def parse_request(self, text: str) -> Tuple[Request, int]:
        request_line = text.splitlines()[0]
        request_line = request_line.rstrip('\r\n')
        request_method, path, http_version = request_line.split()
        assert(http_version == "HTTP/1.1")
        request = Request(http_method=request_method, resource=path)
        expecting = 0
        return request, expecting


