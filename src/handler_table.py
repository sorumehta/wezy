from typing import Callable, Dict, Tuple, Optional, Any
from request import Request

handler_map = {}


def get_key(method: str, resource: str):
    return f"{method}:{resource}"


def insert_handler(method: str, resource: str, func: Callable[[Request], Dict[str, Any]]) -> None:
    key = get_key(method, resource)
    handler_map[key] = func


def find_handler(http_method: str, resource: str) -> Tuple[Optional[Callable[[Request], Dict[str, Any]]], Dict[str, str]]:
    # TODO: handle path parameters
    # dictionary lookup assumes the request path doesn't have path parameters
    key = get_key(http_method, resource)
    if key in handler_map:
        return handler_map[key], {}
    return None, {}
