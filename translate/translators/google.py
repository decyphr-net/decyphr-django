from typing import Any, Self

from django.conf import settings
from google.cloud import translate_v2 as translate
from google.oauth2 import service_account


class GoogleTranslator:
    api_key: str | None
    secret_key: str | None

    def __init__(
        self: Self, api_key: str | None = None, secret_key: str | None = None
    ) -> None:
        self.api_key = api_key
        self.secret_key = secret_key

    def initialise_client(self: Self):
        return translate.Client(
            credentials=service_account.Credentials.from_service_account_file(
                filename=settings.GOOGLE_CLOUD_CRED_FILE_NAME,
                scopes=settings.GOOGLE_CLOUD_SCOPES,
            )
        )

    def translate(
        self: Self, text: str, target_lang: str, source_lang: str | None = None
    ) -> Any:
        return self.initialise_client().translate(
            text, target_language=target_lang, source_language=source_lang
        )

    def get_translated_text(
        self: Self, text: str, target_lang: str, source_lang: str | None = None
    ) -> str:
        return self.translate(
            text=text, target_lang=target_lang, source_lang=source_lang
        )["translatedText"]  # type: ignore
