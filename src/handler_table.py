from typing import Callable, Dict, Tuple, Optional, Any
from request import Request


def test_handler(request: Request):
    print("processing request from test handler")
    return {"body": "test successful", "headers": [("Key1", "val1")]}


handler_map = {"test": test_handler}


def find_handler(http_method: str, resource: str) -> Tuple[Optional[Callable[[Request], Dict[str, Any]]], Dict[str, str]]:
    print("NOTIMPLEMENTED: find_handler")
    if "test" in handler_map:
        return handler_map["test"], {}
    return None, {}
