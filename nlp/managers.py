# type: ignore
from typing import Self, Type

from nlp.entities import ProcessorParams, TextPiece
from nlp.exceptions import NLPValidationException
from nlp.models import TextPiece as TextPieceModel
from nlp.processors import get_processor
from nlp.serializers import Deserializer, Serializer
from preferences.models import Preferences


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

    def _create_db_instances(
        self: Self, processed_data: list[TextPiece]
    ) -> list[TextPieceModel]:
        """Create DB Instances

        Iterate over the data provided and store each item in the DB and return a list
        of the DB instances

        Args:
            list[TextPiece]: The processed data

        Returns:
            list[TextPieceModel]: The DB instances
        """
        text_pieces = []
        for processed_text_piece in processed_data:
            text_piece = TextPieceModel(
                text=processed_text_piece.text_item,
                pos_tag=processed_text_piece.pos_tag,
                language=processed_text_piece.language,
            )
            text_piece.save()
            text_pieces.append(text_piece)
        return text_pieces

    def _process(self: Self, params: ProcessorParams) -> list[TextPieceModel]:
        """Process

        Get the processor and use the text and language info to the process the data.
        Once the data has been processed, store it in the DB and return it the instances

        Args:
            params (ProcessorParams): The data needed to determine the process to be
                used, along with the text and the language

        Returns:
            list[TextPieceModel]
        """
        processed_text_pieces = get_processor(params.processor).process(
            params.text, params.language
        )

        return self._create_db_instances(processed_data=processed_text_pieces)

    def create_new_processed_text(
        self: Self, request_data: dict[str, str]
    ) -> Serializer:
        """Create new processed text

        Handle the nlp endpoint and generate the part of speech tagging for the text
        provided and store it in the DB

        Args:
            request_data (dict[str, str]): The body of the POST request

        returns:
            Serializer: The serialized `TextPiece` data
        """
        deserializer = self.deserializer(data=request_data)

        if not deserializer.is_valid():
            raise NLPValidationException(errors=deserializer.errors)

        processor_params = ProcessorParams(
            preferences=Preferences.objects.all().first(),
            text=deserializer.data["text_to_be_processed"],
            language_code=deserializer.data.get("language_code", None),
            processor=deserializer.data.get("processor", None),
        )

        return self.serializer(self._process(processor_params), many=True)
