# type: ignore
from typing import Self, Type

from languages.models import Language
from translate.exceptions import TranslationValidationException
from translate.serializers import Deserializer, Serializer
from translate.translators import get_translator


class TranslationManager:
    deserializer: Type[Deserializer]
    serializer: Type[Serializer]

    def __init__(
        self: Self,
        deserializer: Type[Deserializer],
        serializer: Type[Serializer],
    ) -> None:
        self.deserializer = deserializer
        self.serializer = serializer

    def _translate(
        self: Self,
        text_to_be_translated: str,
        source_language: Language,
        target_language: Language,
        translator: str,
    ) -> str:
        """Translate

        Acts as the interface into the protocol. Gets the relevant translator based on
        the string provided by the client and gets the translated text based on the
        text, target/source langs and tranlsation provider requested.

        Args:
            text_to_be_translated (str): Text to translate
            target_lang (Language): The Language record containing the relevant data
                for the target language
            source_lang (Language): The Language record containing the relevant data
                for the source language
            translator (str): The name of the translator to use
        """
        return get_translator(translator).get_translated_text(
            text_to_be_translated,
            target_language,
            source_language,
        )

    def create_new_translation(self: Self, request_data: dict[str, str]) -> Serializer:
        """Create new translation

        Validates and deserialises the data received by the end point and translates
        the text based on the provided request data. This will then create a new
        translation record in the DB and return that back to the caller

        Args:
            request_data (dict[str, str]): The data received by the endpoint

        Returns:
            Serializer: The serialised `Translation` instance
        """
        deserializer = self.deserializer(data=request_data)

        if not deserializer.is_valid():
            raise TranslationValidationException(errors=deserializer.errors)

        source_language = Language.language_manager.get_by_long_code_or_short_code(
            deserializer.data["source_language_code"],
        )

        target_language = Language.language_manager.get_by_long_code_or_short_code(
            deserializer.data["target_language_code"]
        )

        translated_text = self._translate(
            text_to_be_translated=deserializer.data["text_to_be_translated"],
            source_language=source_language,
            target_language=target_language,
            translator=deserializer.data["translator"],
        )

        translation = self.serializer(
            data={
                "source_text": deserializer.data["text_to_be_translated"],
                "translated_text": translated_text,
                "source_language": source_language.id,
                "target_language": target_language.id,
            }
        )

        if not translation.is_valid():
            raise TranslationValidationException(errors=translation.errors)

        translation.save()
        return translation
