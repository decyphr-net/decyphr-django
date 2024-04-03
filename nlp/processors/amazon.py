from typing import Any, Self

from boto3 import client

from languages.models import Language
from nlp.entities import TextPiece


class AmazonNLP:
    api_key: str
    secret_key: str | None
    region: str

    def __init__(
        self: Self, aws_access_key_id: str, aws_secret_access_key: str, aws_region: str
    ) -> None:
        self.api_key = aws_access_key_id
        self.secret_key = aws_secret_access_key
        self.region = aws_region

    def parse_text(self: Self, response: dict[str, Any]) -> list[TextPiece]:
        return [
            TextPiece(text_item=item["Text"], pos_tag=item["PartOfSpeech"]["Tag"])
            for item in response["SyntaxTokens"]
        ]

    def process(self: Self, text: str, language: Language) -> list[TextPiece]:
        comprehend = client(
            "comprehend",
            region_name=self.region,
            aws_access_key_id=self.api_key,
            aws_secret_access_key=self.secret_key,
        )
        return self.parse_text(
            comprehend.detect_syntax(Text=text, LanguageCode=language.short_code)
        )
