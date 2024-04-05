# type: ignore
from typing import Self, Type

from preferences.models import Preferences
from translate.entities import TranslatorParams
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

    def _translate(self: Self, params: TranslatorParams) -> str:
        """Translate

        Acts as the interface into the protocol. Gets the relevant translator based on
        the string provided by the client and gets the translated text based on the
        text, target/source langs and tranlsation provider requested.

        Args:
            params (TranslatorParams): The data required in order to be able
                to perform the translation
        """
        return get_translator(params.translator).get_translated_text(
            params.text,
            params.target_language,
            params.source_language,
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

        translator_params = TranslatorParams(
            preferences=Preferences.objects.all().first(),
            text=deserializer.data["text_to_be_translated"],
            translator=deserializer.data.get("translator", None),
            source_language_code=deserializer.data.get("source_language_code", None),
            target_language_code=deserializer.data.get("target_language_code", None),
        )

        translated_text = self._translate(translator_params)

        translation = self.serializer(
            data={
                "source_text": translator_params.text,
                "translated_text": translated_text,
                "source_language": translator_params.source_language.id,
                "target_language": translator_params.target_language.id,
            }
        )

        if not translation.is_valid():
            raise TranslationValidationException(errors=translation.errors)

        translation.save()
        return translation
