from typing import Self

from django.db import models


class LanguageModelManager(models.Manager):
    def get_by_long_code_or_short_code(self: Self, code: str) -> "Language":
        """Get by long code or short code

        Try to get a language by its `code` and if that fails, try to get the
        `short_code`.

        NOTE: In the event that the code cannot be matched and the `short_code` is
            needed, the first occurence will be returned. This behaviour may need to be
            revised in the future

        Args:
            code (str): The code to perform the match on

        Returns:
            Language: The relevant language record
        """
        try:
            return super().get_queryset().get(code__iexact=code)
        except Language.DoesNotExist:
            return super().get_queryset().filter(short_code__iexact=code).first()  # type: ignore


class Language(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    code = models.CharField(max_length=8, blank=False, null=False)
    short_code = models.CharField(max_length=2, blank=False, null=False)
    description = models.TextField(blank=False, null=False)

    language_manager = LanguageModelManager()

    def __str__(self: Self) -> str:
        return self.name
