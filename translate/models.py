from typing import Self

from django.db import models

from languages.models import Language


class Translation(models.Model):
    source_text = models.TextField()
    translated_text = models.TextField()
    source_language = models.ForeignKey(
        Language, on_delete=models.CASCADE, related_name="source_language"
    )
    target_language = models.ForeignKey(
        Language, on_delete=models.CASCADE, related_name="target_language"
    )

    def __str__(self: Self) -> str:
        return f"{self.source_text} -> {self.translated_text}"
