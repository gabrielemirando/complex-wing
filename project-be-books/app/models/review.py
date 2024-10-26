from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    id = models.UUIDField(primary_key=True)
    score = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ],
    )
    content = models.TextField(max_length=500)
    book_id = models.PositiveIntegerField()
    book_title = models.TextField(default="")
    book_authors = models.JSONField(default=list)
    book_subjects = models.JSONField(default=list)
