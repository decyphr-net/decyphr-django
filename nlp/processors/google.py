# type: ignore
from typing import Self

from django.conf import settings
from google.cloud.language import Document, LanguageServiceClient
from google.oauth2 import service_account

from languages.models import Language
from nlp.entities import TextPiece


class GoogleNLP:
    api_key: str | None
    secret_key: str | None

    def __init__(
        self: Self, api_key: str | None = None, secret_key: str | None = None
    ) -> None:
        self.api_key = api_key
        self.secret_key = secret_key

    def initialise_client(self: Self):
        return LanguageServiceClient(
            credentials=service_account.Credentials.from_service_account_file(
                filename=settings.GOOGLE_CLOUD_CRED_FILE_NAME,
                scopes=settings.GOOGLE_CLOUD_SCOPES,
            )
        )

    def parse_response(
        self: Self, response: dict[str, str], language: Language
    ) -> list[TextPiece]:
        return [
            TextPiece(
                text_item=token.text.content,
                pos_tag=token.part_of_speech.tag.name,
                language=language,
            )
            for token in response.tokens
        ]

    def process(self: Self, text: str, language: Language) -> list[TextPiece]:
        return self.parse_response(
            self.initialise_client().analyze_syntax(
                document=Document(content=text, type_=Document.Type.PLAIN_TEXT)
            ),
            language,
        )
