from typing import Self
from unittest.mock import patch

from django.test import TestCase

from languages.models import Language
from translate.managers import TranslationManager
from translate.models import Translation
from translate.serializers import Deserializer, Serializer


class TanslationManagerTestCase(TestCase):
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

    @patch("translate.views.TranslationManager._translate")
    def test_create_new_translation(self: Self, mock_translate) -> None:
        mock_translate.return_value = "Hi"
        manager = TranslationManager(Deserializer, Serializer)
        data = {
            "text_to_be_translated": "Hello",
            "target_language_code": "pt",
            "source_language_code": "en",
            "translator": "amazon",
        }
        actual_translation = manager.create_new_translation(data).data

        expected_translation = {
            "id": 2,
            "source_text": "Hello",
            "translated_text": "Hi",
            "source_language": 2,
            "target_language": 1,
        }

        self.assertEqual(actual_translation, expected_translation)
