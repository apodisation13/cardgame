from django.db import models

from apps.core.models import Color, Faction


class Type(models.Model):
    """тип карты - Unit, Special"""
    name = models.CharField(max_length=32, blank=False, null=False, unique=True)

    def __str__(self):
        return f'{self.id} - {self.name}'


class Ability(models.Model):
    """способность карты"""
    name = models.CharField(max_length=32, blank=False, null=False, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.id} - {self.name}'


class PassiveAbility(models.Model):
    """пассивные способности карт и лидеров"""
    name = models.CharField(max_length=64, blank=False, null=False, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.id} - {self.name}'


class Card(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False, unique=True)
    unlocked = models.BooleanField(default=True)  # True - unlocked, False - locked
    faction = models.ForeignKey(Faction, related_name='cards',
                                on_delete=models.PROTECT)
    color = models.ForeignKey(Color, related_name='cards',
                              on_delete=models.PROTECT)
    type = models.ForeignKey(Type, related_name='cards',
                             on_delete=models.PROTECT)
    ability = models.ForeignKey(Ability, related_name='cards',
                                on_delete=models.PROTECT)
    charges = models.IntegerField(default=1, blank=False, null=False)
    damage = models.IntegerField(default=0, blank=False, null=False)
    hp = models.IntegerField(default=0, blank=False, null=False)
    heal = models.IntegerField(default=0, blank=False, null=False)
    image = models.ImageField(upload_to='cards/', blank=True, null=True)
    has_passive = models.BooleanField(default=False)
    passive_ability = models.ForeignKey(PassiveAbility, related_name='cards',
                                        on_delete=models.PROTECT,
                                        blank=True, null=True, default=None)

    def __str__(self):
        return f'{self.id} {self.name}, hp {self.hp}, ' \
               f'ability {self.ability}, damage {self.damage}, heal {self.heal} '

    class Meta:
        ordering = ("-color", "-damage", "-hp", "-charges")


class CardDeck(models.Model):
    """Связи колод и карт в них"""
    card = models.ForeignKey("Card", related_name="d", on_delete=models.CASCADE)
    deck = models.ForeignKey("Deck", related_name="d", on_delete=models.CASCADE)


class Deck(models.Model):
    """Модель колоды"""
    name = models.CharField(max_length=32, blank=False, null=False)
    cards = models.ManyToManyField(Card,
                                   related_name="cards",
                                   through=CardDeck)
    health = models.IntegerField(blank=False, null=False, default=0)
    leader = models.ForeignKey("Leader", related_name="decks",
                               on_delete=models.CASCADE,
                               blank=True, null=True, default=None)

    def __str__(self):
        return f'{self.id}, health {self.health}, {self.leader}'


class Leader(models.Model):
    name = models.CharField(max_length=32, blank=False, null=False, unique=True)
    unlocked = models.BooleanField(default=True)  # True - unlocked, False - locked
    faction = models.ForeignKey(Faction, related_name="leaders",
                                on_delete=models.CASCADE)
    ability = models.ForeignKey(Ability, related_name='leaders',
                                on_delete=models.PROTECT)
    damage = models.IntegerField(default=0, blank=False, null=False)
    charges = models.IntegerField(default=1, blank=False, null=False)
    image = models.ImageField(upload_to='leaders/', blank=True, null=True)
    has_passive = models.BooleanField(default=False)
    passive_ability = models.ForeignKey(PassiveAbility, related_name='leaders',
                                        on_delete=models.PROTECT,
                                        blank=True, null=True, default=None)

    def __str__(self):
        return f'{self.name}, ability {self.ability}, damage {self.damage} charges {self.charges}'

    class Meta:
        ordering = ("faction", "-damage")
