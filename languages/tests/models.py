from typing import Self

from django.test import TestCase

from languages.models import Language


class ModelManagerTestCase(TestCase):
    def setUp(self: Self) -> None:
        Language.language_manager.create(
            name="Brazilian Portuguese",
            code="PT-BR",
            short_code="PT",
            description="Language spoken in Brazil",
        )

    def test_get_by_long_code_or_short_code_with_code(self: Self) -> None:
        language = Language.language_manager.get_by_long_code_or_short_code("PT-BR")
        self.assertEqual(language, Language.language_manager.get(code__iexact="PT-BR"))

    def test_get_by_long_code_or_short_code_with_short_code(self: Self) -> None:
        language = Language.language_manager.get_by_long_code_or_short_code("PT")
        self.assertEqual(
            language, Language.language_manager.get(short_code__iexact="PT")
        )
