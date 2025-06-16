from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    GENDER_CHOICES = (
        ("М", "Мужской"),
        ("Ж", "Женский"),
    )
    pol = models.CharField("Пол", max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    vozrast = models.IntegerField("Возраст", blank=True, null=True)
    ves = models.FloatField("Вес (кг)", blank=True, null=True)
    rost = models.FloatField("Рост (см)", blank=True, null=True)

    def __str__(self):
        return self.email or self.username
