from django.db import models

from apps.accounts.models import CustomUser
from apps.core.models import Ability, Color, Faction, PassiveAbility, Type


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
    has_passive_in_hand = models.BooleanField(default=False)
    passive_ability = models.ForeignKey(PassiveAbility, related_name='cards',
                                        on_delete=models.PROTECT,
                                        blank=True, null=True, default=None)
    timer = models.IntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return f'{self.id} {self.name}, hp {self.hp}, ' \
               f'ability {self.ability}, damage {self.damage}, heal {self.heal} '

    class Meta:
        ordering = ("-color", "-damage", "-hp", "-charges")


class Deck(models.Model):
    """???????????? ????????????"""
    name = models.CharField(max_length=32, blank=False, null=False)
    cards = models.ManyToManyField(Card,
                                   related_name="cards",
                                   through="CardDeck")
    health = models.IntegerField(blank=False, null=False, default=0)
    leader = models.ForeignKey("Leader", related_name="decks",
                               on_delete=models.CASCADE,
                               blank=True, null=True, default=None)

    def __str__(self):
        return f'{self.id}, name {self.name}, health {self.health}, {self.leader}'


class CardDeck(models.Model):
    """?????????? ?????????? ?? ???????? ?? ??????"""
    card = models.ForeignKey("Card", related_name="d", on_delete=models.CASCADE)
    deck = models.ForeignKey("Deck", related_name="d", on_delete=models.CASCADE)


class UserCard(models.Model):
    """?????????? ???????????? ?? ????????, ?????????????? ???????? ?? ??????"""
    card = models.ForeignKey(Card, related_name="u_c",
                             on_delete=models.CASCADE,
                             blank=False, null=False)
    user = models.ForeignKey(CustomUser, related_name="u_c",
                             on_delete=models.CASCADE,
                             blank=False, null=False)
    count = models.IntegerField(default=1, blank=False, null=False)


class UserLeader(models.Model):
    """?????????? ???????????? ?? ??????????????, ?????????????? ???????? ?? ??????"""
    leader = models.ForeignKey(Leader, related_name="u_l",
                               on_delete=models.CASCADE,
                               blank=False, null=False)
    user = models.ForeignKey(CustomUser, related_name="u_l",
                             on_delete=models.CASCADE,
                             blank=False, null=False)
    count = models.IntegerField(default=1, blank=False, null=False)


class UserDeck(models.Model):
    """?????????? ???????????? ?? ??????????, ?????????????? ???????? ?? ??????"""
    deck = models.ForeignKey(Deck, related_name="u_d",
                             on_delete=models.CASCADE,
                             blank=False, null=False)
    user = models.ForeignKey(CustomUser, related_name="u_d",
                             on_delete=models.CASCADE,
                             blank=False, null=False)
