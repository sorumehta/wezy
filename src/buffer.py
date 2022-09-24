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
        contents = self.stream_data[:MAX_REQUEST_SIZE]
        self.contents += contents
        self.total_buffered += len(contents)
        if is_line_terminated(self.contents):
            parsed = request.parse_request(self.contents)
            self.request = parsed
            self.contents = None
        return contents[-1]

    def write_response(self, response_code: int = 200, body: str = "",
                       response_headers: Optional[List[Tuple[str, str]]] = None):
        self.response = response.create_response(response_code, body, response_headers)
