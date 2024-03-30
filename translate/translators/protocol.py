# type: ignore
from typing import Any, Protocol, Self

from languages.models import Language


class TranslatorProtocol(Protocol):
    api_key: str
    secret_key: str | None

    def translate(
        self: Self,
        text: str,
        target_lang: Language,
        source_lang: Language | None = None,
    ) -> Any:
        """Translate

        Translate the given text using to the target language.

        As some translation providers required different formats of the language codes,
        accept the lang instances so that any implementions of this protocol can act on
        that data accordingly

        Args:
            text (str): Text to translate
            target_lang (Language): The Language record containing the relevant data
                for the target language
            source_lang (Language): The Language record containing the relevant data
                for the source language

        Returns:
            The data returned from the API
        """

    def get_translated_text(
        self: Self,
        text: str,
        target_lang: Language,
        source_lang: Language | None = None,
    ) -> str:
        """Get translated text

        Translate the given text to the provided target language and return the
        translated text string.

        As some translation providers required different formats of the language codes,
        accept the lang instances so that any implementions of this protocol can act on
        that data accordingly

        Args:
            text (str): Text to translate
            target_lang (Language): The Language record containing the relevant data
                for the target language
            source_lang (Language): The Language record containing the relevant data
                for the source language

        Returns:
            str: The translated text
        """
