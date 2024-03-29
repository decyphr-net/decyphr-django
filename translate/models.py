from typing import Self

from django.db import models


class Translation(models.Model):
    source_text = models.TextField()
    translated_text = models.TextField()

    def __str__(self: Self) -> str:
        return self.source_text
