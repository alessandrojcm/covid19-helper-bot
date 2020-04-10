from typing import Callable

from fastapi import FastAPI


def create_start_app_handler(app: FastAPI) -> Callable:  # type: ignore
    def start_app() -> None:
        ...

    return start_app
