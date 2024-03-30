# type: ignore
from typing import Any, Self

from boto3 import client

from languages.models import Language


class AmazonTranslator:
    api_key: str
    secret_key: str | None
    region: str

    def __init__(
        self: Self, aws_access_key_id: str, aws_secret_access_key: str, aws_region: str
    ) -> None:
        self.api_key = aws_access_key_id
        self.secret_key = aws_secret_access_key
        self.region = aws_region

    def translate(
        self: Self,
        text: str,
        target_lang: Language,
        source_lang: Language | None = None,
    ) -> Any:
        translate = client(
            "translate",
            region_name=self.region,
            aws_access_key_id=self.api_key,
            aws_secret_access_key=self.secret_key,
        )
        return translate.translate_text(
            Text=text,
            TargetLanguageCode=target_lang.code,
            SourceLanguageCode=source_lang.code,
        )

    def get_translated_text(
        self: Self,
        text: str,
        target_lang: Language,
        source_lang: Language | None = None,
    ) -> str:
        return self.translate(
            text=text, target_lang=target_lang, source_lang=source_lang
        )["TranslatedText"]  # type: ignore
