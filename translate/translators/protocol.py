from typing import Protocol, Self


class TranslatorProtocol(Protocol):
    api_key: str
    secret_key: str | None

    def translate(
        self: Self, text: str, target_lang: str, source_lang: str | None = None
    ) -> str:  # type: ignore
        """Translate

        Translate the given text using to the target language

        Args:
            text (str): Text to translate
            target_lang (str): The ISO identifier for the target language
            source_lang (str): The language of the provided text

        Returns:
            The data returned from the API
        """
        ...

    def get_translated_text(
        self: Self, text: str, target_lang: str, source_lang: str | None = None
    ) -> str:
        """Get translated text

        Translate the given text to the provided target language and return the
        translated text string

        Args:
            text (str): Text to translate
            target_lang (str): The ISO identifier for the target language
            source_lang (str): The language of the provided text

        Returns:
            str: The translated text
        """
        ...
