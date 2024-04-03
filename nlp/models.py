from django.db import models


class TextPiece(models.Model):
    text = models.CharField(max_length=255)
    pos_tag = models.CharField(max_length=255)
