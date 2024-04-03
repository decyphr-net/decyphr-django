# type: ignore
from typing import Self

from django.http import Http404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .exceptions import TranslationValidationException
from .managers import TranslationManager
from .models import Translation
from .serializers import Deserializer, Serializer


class TranslationViewSet(ModelViewSet):
    queryset = Translation.objects.all()
    deserializer_class = Deserializer
    serializer_class = Serializer
    manager = TranslationManager

    def _get_object(self: Self, pk: int) -> Translation:
        """Get object

        Helper method to retrieve a single `Translation` instance.

        Args:
            pk (int): Primary key to retrieve

        Returns:
            Translation: The relevant `Translation` instance

        Raises:
            Http404 is raised if the record doesn't exist in the DB
        """
        try:
            return Translation.objects.get(pk=pk)
        except Translation.DoesNotExist:
            raise Http404

    def retrieve(self: Self, request: Request, pk: int) -> Response:
        """Retrieve

        Retries a single Translation instance and returns it to the client

        Args:
            pk (int): The primary key of the record to be looked up

        Returns:
            Response: 200 if the request completes successfully

        Example Usage:
            http GET http://127.0.0.1:8000/translate/1

        Example Response:
            {
                "source_text": "Hello",
                "translated_text": "Ola"
            }
        """
        return Response(self.serializer_class(self._get_object(pk)).data)

    def create(self: Self, request: Request) -> Response:
        """Create

        Accepts a piece of text and language code and will translate the text to the
        language specified. Then creates the record and returns the translation info
        to the client

        Args:
            request.data (dict[str, str]):
                text_to_be_translated (str): The text to be translated
                source_language_code (str): The ISO representation of the language of
                    text to translate
                target_language_code (str): The ISO representation of the language to
                    translate the text to
                translator (str): The name of the translator to use to translate the
                    text

        Returns:
            Response: 201 if the request completes successfully
            Response: 400 if the data cannot be validated

        Example Usage:
            echo '{
                "text_to_be_translated": "Hello",
                "language_code": "PT-BR"
            }' |  \
            http POST http://127.0.0.1:8000/translate/ \
            Content-Type:application/json

        Example Response:
            {
                "id": 7,
                "source_text": "Hello",
                "translated_text": "Olá"
            }
        """
        manager = self.manager(
            deserializer=self.deserializer_class,
            serializer=self.serializer_class,
        )

        try:
            translation = manager.create_new_translation(request_data=request.data)
        except TranslationValidationException as e:
            return Response(e.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(translation.data, status=status.HTTP_201_CREATED)

    def list(self: Self, request: Request) -> Response:
        """List

        Gets a full list of all Translations in the DB

        Returns:
            Response: 200 with all Translation records if successful

        Example Usage:
            http GET http://127.0.0.1:8000/translate/

        Example Response:
            [
                {
                    "id": 1,
                    "source_text": "Hello",
                    "translated_text": "Ola"
                },
                {
                    "id": 2,
                    "source_text": "Hello",
                    "translated_text": "Ola"
                },
                {
                    "id": 3,
                    "source_text": "Hello",
                    "translated_text": "Olá"
                },
                {
                    "id": 4,
                    "source_text": "Hello",
                    "translated_text": "Olá"
                },
                {
                    "id": 5,
                    "source_text": "Hello",
                    "translated_text": "Olá"
                },
                {
                    "id": 6,
                    "source_text": "Hello",
                    "translated_text": "Olá"
                },
                {
                    "id": 7,
                    "source_text": "Hello",
                    "translated_text": "Olá"
                }
            ]
        """
        return Response(self.get_serializer(self.queryset, many=True).data)

    def delete(self: Self, request: Request, pk: int) -> Response:
        """Delete

        Deletes the Translation based on the provided primary key

        Args:
            pk (int): The primary key of the translation to delete

        Returns:
            Response: 204 if item was successfully deleted

        Example Usage:
            http DELETE http://127.0.0.1:8000/translate/1
        """
        self._get_object(pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
