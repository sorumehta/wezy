import datetime
from email import utils
from http.client import responses
from typing import List, Tuple


class Response:
    def __init__(self, headers: List[Tuple[str, str]] = None, response_code: int = 200,
                 body: str = None, content_type="text/html"):
        self.content_type = content_type
        self.response_headers = headers
        self.response_code = response_code
        self.body = body if body else ""

    def build_response_str(self) -> str:
        rfc_datetime = utils.format_datetime(datetime.datetime.now())
        server_headers = [
            ('Date', f"{rfc_datetime}"),
            ('Server', 'W3ZY 0.1')
        ]
        default_headers = [("Content-Type", self.content_type)]
        headers_to_add = []
        for d_h in default_headers:
            found = False
            for h in self.response_headers:
                if h[0] == d_h[0]:
                    found = True
                    break
            if not found:
                headers_to_add.append(d_h)
        response_headers = server_headers + self.response_headers + headers_to_add
        response = f"HTTP/1.1 {self.response_code} {responses[self.response_code]}\r\n"
        for header in response_headers:
            response += f"{header[0]}: {header[1]}\r\n"
        response += "\r\n"
        response += self.body
        print("built response:")
        print(''.join(
            f'> {line}\n' for line in response.splitlines()
        ))
        return response


def create_response(response_code: int, body: str, response_headers: List[Tuple[str, str]]) -> Response:
    return Response(response_headers, response_code, body)
