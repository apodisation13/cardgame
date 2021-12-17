from django.db import models


class Faction(models.Model):
    name = models.CharField(max_length=32, blank=False, null=False)

    def __str__(self):
        return f'{self.id} - {self.name}'


class Color(models.Model):
    name = models.CharField(max_length=32, blank=False, null=False)

    def __str__(self):
        return f'{self.id} - {self.name}'


class Type(models.Model):
    name = models.CharField(max_length=32, blank=False, null=False)

    def __str__(self):
        return f'{self.id} - {self.name}'


class Ability(models.Model):
    name = models.CharField(max_length=32, blank=False, null=False)

    def __str__(self):
        return f'{self.id} - {self.name}'


class Card(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False)
    faction = models.ForeignKey(Faction, related_name='cards', on_delete=models.PROTECT)
    color = models.ForeignKey(Color, related_name='cards', on_delete=models.PROTECT)
    type = models.ForeignKey(Type, related_name='cards', on_delete=models.PROTECT)
    ability = models.ForeignKey(Ability, related_name='cards', on_delete=models.PROTECT)
    charges = models.IntegerField(default=1, blank=False, null=False)
    hp = models.IntegerField(default=0, blank=False, null=False)
    damage = models.IntegerField(default=0, blank=False, null=False)
    heal = models.IntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return f'{self.name}, hp {self.hp}, ability {self.ability}, damage {self.damage}, heal {self.heal} '
