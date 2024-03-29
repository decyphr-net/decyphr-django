from typing import Self

from boto3 import client

from translate.translators.protocol import TranslatorProtocol


class AmazonTranslator(TranslatorProtocol):
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
        self: Self, text: str, target_lang: str, source_lang: str | None = None
    ) -> str:
        translate = client(
            "translate",
            region_name=self.region,
            aws_access_key_id=self.api_key,
            aws_secret_access_key=self.secret_key,
        )
        return translate.translate_text(
            Text=text, TargetLanguageCode=target_lang, SourceLanguageCode=source_lang
        )

    def get_translated_text(
        self: Self, text: str, target_lang: str, source_lang: str | None = None
    ) -> str:
        return self.translate(
            text=text, target_lang=target_lang, source_lang=source_lang
        )["TranslatedText"]  # type: ignore
