# type: ignore
from typing import Self

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

    def create(self: Self, request: Request, *args, **kwargs) -> Response:
        manager = self.manager(
            deserializer=self.deserializer_class,
            serializer=self.serializer_class,
        )

        try:
            translation = manager.create_new_translation(request_data=request.data)
        except TranslationValidationException as e:
            return Response(e.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(translation.data, status=status.HTTP_201_CREATED)
