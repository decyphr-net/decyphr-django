# type: ignore
from typing import Self

from django.http import Http404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from nlp.exceptions import NLPValidationException
from nlp.managers import NLPManager
from nlp.models import TextPiece
from nlp.serializers import Deserializer, Serializer


class NLPViewSet(ModelViewSet):
    queryset = TextPiece.objects.all()
    deserializer_class = Deserializer
    serializer_class = Serializer
    manager = NLPManager

    def _get_object(self: Self, pk: int) -> TextPiece:
        """Get object

        Helper method to retrieve a single `TextPiece` instance.

        Args:
            pk (int): Primary key to retrieve

        Returns:
            TextPiece: The relevant `TextPiece` instance

        Raises:
            Http404 is raised if the record doesn't exist in the DB
        """
        try:
            return TextPiece.objects.get(pk=pk)
        except TextPiece.DoesNotExist:
            raise Http404

    def retrieve(self: Self, request: Request, pk: int) -> Response:
        """Retrieve

        Retries a single TextPiece instance and returns it to the client

        Args:
            pk (int): The primary key of the record to be looked up

        Returns:
            Response: 200 if the request completes successfully

        Example Usage:
            http GET http://127.0.0.1:8000/nlp/1

        Example Response:
            {
                "id": 1,
                "text": "Olá",
                "pos_tag": "VERB"
            }
        """
        return Response(self.serializer_class(self._get_object(pk)).data)

    def create(self: Self, request: Request) -> Response:
        """Create

        Accepts a piece of text and the assoicated language code. This text will be
        processed and will return a breakdown of the text and the corresponding part of
        speech tags

        Args:
            request.data (dict[str, str]):
                text_to_be_processed (str): The text to be processed
                language_code (str): The ISO representation of the language of the text
                processor (str): The name of the processor to be used

        Returns:
            Response: 201 if the request completes successfully
            Response: 400 if the data cannot be validated

        Example Usage:
            echo '{
                "text_to_be_processed": "Olá, aí! Como você está hoje?",
                "language_code": "pt",
                "processor": "amazon"
            }' |  \
            http POST http://127.0.0.1:8000/nlp/ \
            Content-Type:application/json

        Example Response:
            [
                {
                    "id": 28,
                    "text": "Olá",
                    "pos_tag": "VERB"
                },
                {
                    "id": 29,
                    "text": ",",
                    "pos_tag": "PUNCT"
                },
                {
                    "id": 30,
                    "text": "aí",
                    "pos_tag": "ADV"
                },
                {
                    "id": 31,
                    "text": "!",
                    "pos_tag": "PUNCT"
                },
                {
                    "id": 32,
                    "text": "Como",
                    "pos_tag": "ADV"
                },
                {
                    "id": 33,
                    "text": "você",
                    "pos_tag": "PRON"
                },
                {
                    "id": 34,
                    "text": "está",
                    "pos_tag": "VERB"
                },
                {
                    "id": 35,
                    "text": "hoje",
                    "pos_tag": "ADV"
                },
                {
                    "id": 36,
                    "text": "?",
                    "pos_tag": "PUNCT"
                }
            ]
        """
        manager = self.manager(
            deserializer=self.deserializer_class,
            serializer=self.serializer_class,
        )

        try:
            text_pieces = manager.create_new_processed_text(request_data=request.data)
        except NLPValidationException as e:
            return Response(e.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(text_pieces.data, status=status.HTTP_201_CREATED)

    def list(self: Self, request: Request) -> Response:
        """List

        Gets a full list of all TextPieces in the DB

        Returns:
            Response: 200 with all TextPiece records if successful

        Example Usage:
            http GET http://127.0.0.1:8000/nlp/

        Example Response:
            [
                {
                    "id": 1,
                    "text": "Olá",
                    "pos_tag": "VERB"
                },
                {
                    "id": 2,
                    "text": ",",
                    "pos_tag": "PUNCT"
                },
                {
                    "id": 3,
                    "text": "aí",
                    "pos_tag": "ADV"
                },
                {
                    "id": 4,
                    "text": "!",
                    "pos_tag": "PUNCT"
                },
                {
                    "id": 5,
                    "text": "Como",
                    "pos_tag": "ADV"
                },
                {
                    "id": 6,
                    "text": "você",
                    "pos_tag": "PRON"
                },
                {
                    "id": 7,
                    "text": "está",
                    "pos_tag": "VERB"
                },
            ]
        """
        return Response(self.get_serializer(self.queryset, many=True).data)

    def delete(self: Self, request: Request, pk: int) -> Response:
        """Delete

        Deletes the TextPiece based on the provided primary key

        Args:
            pk (int): The primary key of the TextPiece to delete

        Returns:
            Response: 204 if item was successfully deleted

        Example Usage:
            http DELETE http://127.0.0.1:8000/nlp/1
        """
        self._get_object(pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
