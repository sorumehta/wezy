from http.client import responses


def is_line_terminated(text: str) -> bool:
    return text.endswith('\r\n\r\n')


def get_status_message(status_code: int) -> str:
    return responses[status_code]
