from django.db import models


class Tag(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        indexes = [
            models.Index(fields=['title']),
        ]

    def __str__(self) -> str:
        return self.title
