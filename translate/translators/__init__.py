from django.conf import settings

from translate.translators.amazon import AmazonTranslator
from translate.translators.deepl import DeeplTranslator
from translate.translators.protocol import TranslatorProtocol

translators = {
    "amazon": AmazonTranslator(
        settings.AWS_SECRET_KEY_ID, settings.AWS_SECRET_ACCESS_KEY, settings.AWS_REGION
    ),
    "deepl": DeeplTranslator(settings.DEEPL_API_KEY, None),
}


def get_translator(name: str) -> TranslatorProtocol:
    return translators[name]
