import time
from typing import Tuple, Optional, List

from utils import is_line_terminated
import request
import response
from constants import MAX_REQUEST_SIZE


class Buffer:
    def __init__(self, stream_data=None):
        self.n_tries = 0
        self.contents = None
        self.stream_data = stream_data
        self.total_buffered = 0
        self.start_time = time.time()
        self.request = None
        self.expecting = 0
        self.response = None

    def process_buffer(self):
        self.n_tries += 1
        self.contents = "" if self.contents is None else self.contents
        if not self.stream_data:
            return "EOF!"
        for char in self.stream_data:
            self.contents += char
            self.total_buffered += 1
            if self.request:
                self.expecting -= 1
            if is_line_terminated(self.contents):
                parsed, expected = request.parse_request(self.contents)
                self.request = parsed
                self.expecting = expected
                self.contents = None
                return char
            if self.total_buffered > MAX_REQUEST_SIZE:
                return char

    def write_response(self, response_code: int = 200, body: str = "",
                       response_headers: Optional[List[Tuple[str, str]]] = None):
        self.response = response.create_response(response_code, body, response_headers)
