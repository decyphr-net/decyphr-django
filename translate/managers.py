# type: ignore
from typing import Self, Type

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

    def _translate(self: Self, data: dict) -> str:
        return get_translator(data["translator"]).get_translated_text(
            data["text_to_be_translated"],
            data["target_language_code"],
            data["source_language_code"],
        )

    def create_new_translation(self: Self, request_data: dict) -> Serializer:
        deserializer = self.deserializer(data=request_data)

        if not deserializer.is_valid():
            raise TranslationValidationException(errors=deserializer.errors)

        result = self._translate(deserializer.data)
        translation = self.serializer(
            data={
                "source_text": deserializer.data["text_to_be_translated"],
                "translated_text": result,
            }
        )

        if not translation.is_valid():
            raise TranslationValidationException(errors=translation.errors)

        translation.save()
        return translation
