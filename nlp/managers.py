# type: ignore
from typing import Self, Type

from languages.models import Language
from nlp.exceptions import NLPValidationException
from nlp.models import TextPiece as TextPieceModel
from nlp.processors import get_processor
from nlp.serializers import Deserializer, Serializer


class NLPManager:
    deserializer: Type[Deserializer]
    serializer: Type[Serializer]

    def __init__(
        self: Self,
        deserializer: Type[Deserializer],
        serializer: Type[Serializer],
    ) -> None:
        self.deserializer = deserializer
        self.serializer = serializer

    def _process(
        self: Self, processor_name: str, text: str, language: Language
    ) -> list[TextPieceModel]:
        processed_text_pieces = get_processor(processor_name).process(text, language)
        text_pieces = []
        for processed_text_piece in processed_text_pieces:
            text_piece = TextPieceModel(
                text=processed_text_piece.text_item,
                pos_tag=processed_text_piece.pos_tag,
            )
            text_piece.save()
            text_pieces.append(text_piece)
        return text_pieces

    def create_new_processed_text(
        self: Self, request_data: dict[str, str]
    ) -> Serializer:
        deserializer = self.deserializer(data=request_data)

        if not deserializer.is_valid():
            raise NLPValidationException(errors=deserializer.errors)

        language = Language.language_manager.get_by_long_code_or_short_code(
            deserializer.data["language_code"],
        )

        processed_text = self._process(
            processor_name=deserializer.data["processor"],
            text=deserializer.data["text_to_be_processed"],
            language=language,
        )
        serialized_data = self.serializer(processed_text, many=True)

        # if not serialized_data.is_valid():
        #     raise NLPValidationException(errors=serialized_data.errors)
        return serialized_data
