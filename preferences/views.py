from typing import Self

from django.http import Http404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from preferences.models import Preferences
from preferences.serializers import PreferencesSerializer


class PreferencesViewSet(ModelViewSet):
    queryset = Preferences.objects.all()
    serializer_class = PreferencesSerializer

    def _get_object(self: Self, pk: int) -> Preferences:
        """Get object

        Helper method to retrieve a single `Preferences` instance.

        Args:
            pk (int): Primary key to retrieve

        Returns:
            Preferences: The relevant `Preferences` instance

        Raises:
            Http404 is raised if the record doesn't exist in the DB
        """
        try:
            return Preferences.objects.get(pk=pk)
        except Preferences.DoesNotExist:
            raise Http404

    def list(self: Self, request: Request) -> Response:
        """ """
        return Response(self.get_serializer(self.queryset.first()).data)

    def partial_update(self, request, pk=None):
        preferences = self._get_object(pk)
        serializer = self.serializer_class(preferences, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)
