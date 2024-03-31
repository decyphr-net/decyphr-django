from typing import Self
from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from languages.models import Language
from translate.models import Translation
from translate.serializers import Serializer


class TranslationViewSetAPITestCase(APITestCase):
    def setUp(self: Self) -> None:
        target_language = Language(
            name="Brazilian Portuguese",
            code="PT-BR",
            short_code="PT",
            description="Language spoken in Brazil",
        )
        target_language.save()
        source_language = Language(
            name="Ireland English",
            code="EN-IE",
            short_code="EN",
            description="Language spoken in Ireland",
        )
        source_language.save()

        Translation.objects.create(
            source_text="Hello",
            translated_text="Ola",
            source_language=source_language,
            target_language=target_language,
        )

    def test_list_translations(self: Self) -> None:
        url = reverse("translate-list")

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, Serializer(Translation.objects.all(), many=True).data
        )

    def test_retrieve_translation(self: Self) -> None:
        translation = Translation.objects.all().first()
        url = reverse("translate-detail", args=(translation.id,))

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, Serializer(translation).data)

    def test_delete_translation(self: Self) -> None:
        translation = Translation.objects.all().first()
        url = reverse("translate-detail", args=(translation.id,))

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(Translation.DoesNotExist):
            Translation.objects.get(id=translation.id)

    @patch("translate.views.TranslationManager._translate")
    def test_create_translation(self: Self, mock_translate) -> None:
        mock_translate.return_value = "Ola"
        url = reverse("translate-list")

        data = {
            "text_to_be_translated": "Hello",
            "target_language_code": "pt",
            "source_language_code": "en",
            "translator": "amazon",
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
