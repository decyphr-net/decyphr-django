from typing import Protocol, Self


class TranslatorProtocol(Protocol):
    api_key: str

    def translate(self: Self, text: str, target_lang: str) -> str:  # type: ignore
        """Translate

        Translate the given text using to the target language

        Args:
            text (str): Text to translate
            target_lang (str): The ISO identifier for the target language

        Returns:
            The translated text
        """
        ...
