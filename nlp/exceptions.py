from typing import Self


class NLPValidationException(Exception):
    errors: dict

    def __init__(self: Self, errors: dict) -> None:
        self.errors = errors
