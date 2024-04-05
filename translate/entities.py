from dataclasses import dataclass
from typing import Self

from languages.models import Language
from preferences.models import Preferences


@dataclass(init=False)
class TranslatorParams:
    translator: str
    source_language: Language
    target_language: Language
    text: str

    def __init__(
        self: Self,
        preferences: Preferences,
        text: str,
        translator: str | None,
        source_language_code: str | None,
        target_language_code: str | None,
    ) -> None:
        self.text = text
        self.translator = translator if translator else preferences.translator

        if source_language_code:
            self.source_language = (
                Language.language_manager.get_by_long_code_or_short_code(
                    source_language_code,
                )
            )
        else:
            self.source_language = preferences.source_lang

        if target_language_code:
            self.target_language = (
                Language.language_manager.get_by_long_code_or_short_code(
                    target_language_code,
                )
            )
        else:
            self.target_language = preferences.target_lang
