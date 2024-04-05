from dataclasses import dataclass
from typing import Self

from languages.models import Language
from preferences.models import Preferences


@dataclass
class TextPiece:
    text_item: str
    pos_tag: str
    language: Language


@dataclass(init=False)
class ProcessorParams:
    processor: str
    language: Language
    text: str

    def __init__(
        self: Self,
        preferences: Preferences,
        text: str,
        language_code: str | None,
        processor: str | None,
    ) -> None:
        self.text = text
        self.processor = processor if processor else preferences.processor

        if language_code:
            self.language = Language.language_manager.get_by_long_code_or_short_code(
                language_code,
            )
        else:
            self.language = preferences.target_lang
