# type: ignore
from typing import Self

from deepl import Translator


class DeeplTranslator:
    """Deepl Translator

    The wrapper for the Deepl Translation API for all comminucations with the Deepl
    API
    """

    api_key: str
    secret_key: str | None

    def __init__(self: Self, api_key: str, secret_key: str | None = None) -> None:
        self.api_key = api_key

    def translate(self: Self, text: str, target_lang: str) -> str:
        return Translator(self.api_key).translate_text(text, target_lang=target_lang)

    def get_translated_text(
        self: Self, text: str, target_lang: str, source_lang: str | None = None
    ) -> str:
        return self.translate(text, target_lang=target_lang).text
