from typing import Callable, Dict, Tuple, Optional


def test_handler():
    print("processing request")


handler_map = {"test": test_handler}


def find_handler(http_method: str, resource: str) -> Tuple[Optional[Callable], Dict[str, str]]:
    print("NOTIMPLEMENTED: find_handler")
    if "test" in handler_map:
        return handler_map["test"], {}
    return None, {}
