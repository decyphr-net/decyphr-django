# type: ignore
from typing import Any, Self

from deepl import Translator

from languages.models import Language


class DeeplTranslator:
    """Deepl Translator

    The wrapper for the Deepl Translation API for all comminucations with the Deepl
    API
    """

    api_key: str
    secret_key: str | None

    def __init__(self: Self, api_key: str, secret_key: str | None = None) -> None:
        self.api_key = api_key
        self.secret = secret_key

    def translate(
        self: Self,
        text: str,
        target_lang: Language,
        source_lang: Language | None = None,
    ) -> Any:
        return Translator(self.api_key).translate_text(
            text, target_lang=target_lang.code
        )

    def get_translated_text(
        self: Self,
        text: str,
        target_lang: Language,
        source_lang: Language | None = None,
    ) -> str:
        return self.translate(text, target_lang=target_lang).text
