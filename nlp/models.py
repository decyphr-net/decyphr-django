from django.db import models

from languages.models import Language


class TextPiece(models.Model):
    text = models.CharField(max_length=255)
    pos_tag = models.CharField(max_length=255)
    language = models.ForeignKey(
        Language, on_delete=models.CASCADE, related_name="language"
    )
