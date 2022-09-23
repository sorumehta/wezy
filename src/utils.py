def is_line_terminated(contents: str)->bool:
    return contents[-4:].startswith("\r\n\r\n")
