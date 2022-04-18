from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.cards.models import Card


class CustomUser(AbstractUser):

    def save(self, *args, **kwargs):

        super(CustomUser, self).save(*args, **kwargs)
        print(self)
        print(self.id)
        cards = Card.objects.all()
        print(cards[:10])

    email = models.EmailField("email", blank=False, unique=True)
