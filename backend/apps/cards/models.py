from django.db import models


class Faction(models.Model):
    """модель фракции - пока Soldiers, Animals, Monsters"""
    name = models.CharField(max_length=32, blank=False, null=False)

    def __str__(self):
        return f'{self.id} - {self.name}'


class Color(models.Model):
    """цвет карты - Bronze, Silver, Gold"""
    name = models.CharField(max_length=32, blank=False, null=False)

    def __str__(self):
        return f'{self.id} - {self.name}'


class Type(models.Model):
    """тип карты - Unit, Special"""
    name = models.CharField(max_length=32, blank=False, null=False)

    def __str__(self):
        return f'{self.id} - {self.name}'


class Ability(models.Model):
    """способность карты"""
    name = models.CharField(max_length=32, blank=False, null=False)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.id} - {self.name}'


class Card(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False)
    faction = models.ForeignKey(Faction, related_name='cards', on_delete=models.PROTECT)
    color = models.ForeignKey(Color, related_name='cards', on_delete=models.PROTECT)
    type = models.ForeignKey(Type, related_name='cards', on_delete=models.PROTECT)
    ability = models.ForeignKey(Ability, related_name='cards', on_delete=models.PROTECT)
    charges = models.IntegerField(default=1, blank=False, null=False)
    damage = models.IntegerField(default=0, blank=False, null=False)
    hp = models.IntegerField(default=0, blank=False, null=False)
    heal = models.IntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return f'{self.name}, hp {self.hp}, ability {self.ability}, damage {self.damage}, heal {self.heal} '


class CardDeck(models.Model):
    """связи колод и карт в них"""
    card = models.ForeignKey("Card", related_name="d", on_delete=models.CASCADE)
    deck = models.ForeignKey("Deck", related_name="d", on_delete=models.CASCADE)


class Deck(models.Model):
    """модель колоды"""
    name = models.CharField(max_length=32, blank=False, null=False)
    cards = models.ManyToManyField(Card, related_name="cards", through=CardDeck)
    health = models.IntegerField(blank=False, null=False, default=0)
    leader = models.ForeignKey("Leader", related_name="decks", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id}, health {self.health}, {self.leader}'


class Leader(models.Model):
    name = models.CharField(max_length=32, blank=False, null=False)
    faction = models.ForeignKey(Faction, related_name="leaders", on_delete=models.CASCADE)
    ability = models.ForeignKey(Ability, related_name='leaders', on_delete=models.PROTECT)
    damage = models.IntegerField(default=0, blank=False, null=False)
    charges = models.IntegerField(default=1, blank=False, null=False)
    passive = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}, ability {self.ability}, damage {self.damage} charges {self.charges}'
