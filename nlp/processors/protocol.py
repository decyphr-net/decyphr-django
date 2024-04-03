from typing import Any, Protocol, Self

from languages.models import Language


class NLPProtocol(Protocol):
    def process(self: Self, text: str, language: Language) -> Any: ...
