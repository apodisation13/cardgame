from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.cards.models import Card


# class CustomUserManager(models.Manager):
#
#     def create_user(self, **kwargs):
#         user = self.create(**kwargs)
#         print(user.id, user.username, user.email)
#         print(111111)
#         return user


class CustomUser(AbstractUser):

    email = models.EmailField("email", blank=False, unique=True)
    cards = models.ManyToManyField(Card,
                                   related_name="cards_users",
                                   through="CardUser")

    # # objects = CustomUserManager()

    def save(self, *args, **kwargs):

        # first_time = False
        print(self.id)

        # сюда идём если пользователь создаётся первый раз!

        super(CustomUser, self).save(*args, **kwargs)
        # first_time = True
        return

        unlocked_cards = Card.objects.filter(unlocked=True).all()

        for card in unlocked_cards:
            carduser = CardUser.objects.filter(card_id=card.id, user_id=self.id).first()
            if not carduser:
                CardUser.objects.create(card_id=card.id, user_id=self.id)
                print(f'Для юзера {self.id}, {self.username} открыли карту {card.id}')
            else:
                print('Такая карта у него уже есть')

        cards = CardUser.objects.filter(user_id=self.id).all()
        print(len(cards))

        if not first_time:
            super(CustomUser, self).save(*args, **kwargs)


class CardUser(models.Model):
    card = models.ForeignKey(Card, related_name="u",
                             on_delete=models.CASCADE,
                             blank=False, null=False)
    user = models.ForeignKey(CustomUser, related_name="u",
                             on_delete=models.CASCADE,
                             blank=False, null=False)

    class Meta:
        unique_together = ('card_id', 'user_id')
