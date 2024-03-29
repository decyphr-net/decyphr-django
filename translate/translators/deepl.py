# type: ignore
from typing import Self

from deepl import Translator

from .protocol import TranslatorProtocol


class DeeplTranslator(TranslatorProtocol):
    """Deepl Translator

    The wrapper for the Deepl Translation API for all comminucations with the Deepl
    API
    """

    api_key: str
    translator: Translator

    def __init__(self: Self, api_key: str) -> None:
        self.api_key = api_key
        self.translator = Translator(self.api_key)

    def translate(self: Self, text: str, target_lang: str) -> str:
        return self.translator.translate_text(text, target_lang=target_lang).text
