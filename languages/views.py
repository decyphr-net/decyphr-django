# type: ignore
from typing import Self

from django.http import Http404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from languages.models import Language
from languages.serializers import LanguageSerializer


class LanguageViewSet(ModelViewSet):
    queryset = Language.language_manager.all()
    serializer_class = LanguageSerializer

    def _get_object(self: Self, pk: int) -> Language:
        """Get object

        Helper method to retrieve a single `Language` instance.

        Args:
            pk (int): Primary key to retrieve

        Returns:
            Language: The relevant `Language` instance

        Raises:
            Http404 is raised if the record doesn't exist in the DB
        """
        try:
            return self.queryset.get(pk=pk)
        except Language.DoesNotExist:
            raise Http404

    def retrieve(self: Self, request: Request, pk: int) -> Response:
        """Retrieve

        Retries a single Language instance and returns it to the client

        Args:
            pk (int): The primary key of the record to be looked up

        Returns:
            Response: 200 if the request completes successfully

        Example Usage:
            http GET http://127.0.0.1:8000/languages/1

        Example Response:
            {
                "id": 1,
                "name": "UK English",
                "code": "EN-GB",
                "short_code": "en",
                "description": "The language spoken in the UK"
            }
        """
        return Response(self.serializer_class(self._get_object(pk)).data)

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
                    "name": "UK English",
                    "code": "EN-GB",
                    "short_code": "en",
                    "description": "The language spoken in the UK"
                },
                {
                    "id": 2,
                    "name": "Brazilian Portuguese",
                    "code": "PT-BR",
                    "short_code": "pt",
                    "description": "The language spoken in Brazil"
                },
                {
                    "id": 3,
                    "name": "English (Ireland)",
                    "code": "en-ie",
                    "short_code": "en",
                    "description": "Language spoken in Ireland"
                }
            ]
        """
        return Response(self.get_serializer(self.queryset, many=True).data)
