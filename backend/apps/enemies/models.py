from django.db import models

from apps.cards.models import Color, Faction

LEVEL_DIFFICULTY_CHOICES = (
    ('easy', 'easy'),
    ('normal', 'normal'),
    ('hard', 'hard'),
)


class Move(models.Model):
    """способность ходить - down, stand, random"""
    name = models.CharField(max_length=64, blank=False, null=False)

    def __str__(self):
        return f'{self.id} - {self.name}'


class Enemy(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False)
    faction = models.ForeignKey(Faction, related_name='enemies', on_delete=models.PROTECT)
    color = models.ForeignKey(Color, related_name='enemies', on_delete=models.PROTECT)
    damage = models.IntegerField(default=0, blank=False, null=False)
    hp = models.IntegerField(default=0, blank=False, null=False)
    image = models.ImageField(upload_to='enemies/', blank=True, null=True)
    move = models.ForeignKey(Move, related_name='enemies', on_delete=models.PROTECT)
    shield = models.BooleanField(default=False)  # щит, есть или нет, по умолчанию нет

    def __str__(self):
        return f'{self.id}:{self.name}, {self.faction}, {self.color}, ' \
               f'damage {self.damage}, hp {self.hp}, move {self.move.name}, shield {self.shield}'


class Level(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False)
    starting_enemies_number = models.IntegerField(default=3, blank=False, null=False)  # сколько в начале появляется
    difficulty = models.CharField(choices=LEVEL_DIFFICULTY_CHOICES, blank=False, null=False, max_length=20)
    enemies = models.ManyToManyField(Enemy, through='LevelEnemy', related_name='levels')

    def __str__(self):
        return f'{self.id}:{self.name}, появление: {self.starting_enemies_number}, ' \
               f'сложность {self.difficulty}, врагов {len(self.l.all())}'


class LevelEnemy(models.Model):
    level = models.ForeignKey(Level, related_name='l', on_delete=models.CASCADE)
    enemy = models.ForeignKey(Enemy, related_name='l', on_delete=models.CASCADE)
