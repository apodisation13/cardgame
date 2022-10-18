from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.accounts.utils import set_unlocked_cards


class CustomUser(AbstractUser):
    email = models.EmailField("email", unique=True)
    cards = models.ManyToManyField("cards.Card",
                                   related_name="user_cards",
                                   through="cards.UserCard")
    leaders = models.ManyToManyField("cards.Leader",
                                     related_name="user_leaders",
                                     through="cards.UserLeader")
    decks = models.ManyToManyField("cards.Deck",
                                   related_name="user_decks",
                                   through="cards.UserDeck")
    levels = models.ManyToManyField("enemies.Level",
                                    related_name="user_levels",
                                    through="enemies.UserLevel")
    scraps = models.IntegerField(default=1000, blank=False, null=False)
    wood = models.IntegerField(default=1000, blank=False, null=False)
    kegs = models.IntegerField(default=3, blank=False, null=False)
    big_kegs = models.IntegerField(default=1, blank=False, null=False)
    chests = models.IntegerField(default=0, blank=False, null=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password", "username"]

    def save(self, *args, **kwargs):
        # если юзер создаётся первый раз, то self.if=None, то открываем ему все карты
        if not self.id:
            super(CustomUser, self).save(*args, **kwargs)
            set_unlocked_cards(self)
            return

        super(CustomUser, self).save(*args, **kwargs)
