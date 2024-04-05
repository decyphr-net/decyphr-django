from django.db import models

from languages.models import Language

SUPPORTED_TRANSLATORS = (
    ("amazon", "Amazon"),
    ("deepl", "Deepl"),
    ("google", "Goolge"),
)

SUPPORTED_NLP_PROCESSORS = (
    ("amazon", "Amazon"),
    ("google", "Google"),
)


class Preferences(models.Model):
    translator = models.CharField(max_length=255, choices=SUPPORTED_TRANSLATORS)
    processor = models.CharField(max_length=255, choices=SUPPORTED_NLP_PROCESSORS)
    source_lang = models.ForeignKey(
        Language, on_delete=models.CASCADE, related_name="source_lang"
    )
    target_lang = models.ForeignKey(
        Language, on_delete=models.CASCADE, related_name="target_lang"
    )
