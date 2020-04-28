from typing import Dict, Any
from abc import ABC

from requests import Response, get, post


class APIService(ABC):
    """
    Base class that abstract away HTTP calls and has some overloads and common parameters
    """

    base_url: str

    def __init__(self, url: str):
        self.base_url = url

    def get(self, path: str, params: Dict[str, Any] = None) -> Response:
        if params is not None:
            return get(**self.__common_params(path, params))
        return get(self.base_url + path, headers={"Content-Type": "application/json"},)

    def post(self, path: str, params: Dict[str, str]) -> Response:
        return post(**self.__common_params(path, params))

    def __common_params(self, path: str, params: Dict[str, Any]) -> dict:
        return {
            "url": self.base_url + path,
            "params": params,
            "headers": {"Content-Type": "application/json"},
        }
