from django.conf import settings

from nlp.processors.amazon import AmazonNLP
from nlp.processors.google import GoogleNLP
from nlp.processors.protocol import NLPProtocol

processors = {
    "amazon": AmazonNLP(
        settings.AWS_SECRET_KEY_ID, settings.AWS_SECRET_ACCESS_KEY, settings.AWS_REGION
    ),
    "google": GoogleNLP(),
}


def get_processor(name: str) -> NLPProtocol:
    return processors[name]
