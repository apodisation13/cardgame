from django.db import models


class Faction(models.Model):
    """модель фракции - пока Neutral, Soldiers, Animals, Monsters """
    name = models.CharField(max_length=32, blank=False, null=False, unique=True)

    def __str__(self):
        return f'{self.id} - {self.name}'


class Color(models.Model):
    """цвет карты - Bronze, Silver, Gold"""
    name = models.CharField(max_length=32, blank=False, null=False, unique=True)

    def __str__(self):
        return f'{self.id} - {self.name}'
