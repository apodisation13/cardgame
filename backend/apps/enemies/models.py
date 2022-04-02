from django.db import models

from apps.core.models import Color, Faction

LEVEL_DIFFICULTY_CHOICES = (
    ('easy', 'easy'),
    ('normal', 'normal'),
    ('hard', 'hard'),
)


class Move(models.Model):
    """
    способность ходить:
    down,
    stand,
    random
    """
    name = models.CharField(max_length=64, blank=False, null=False, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.id} - {self.name}'


class EnemyPassiveAbility(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.id} - {self.name}'


class Enemy(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False, unique=True)
    faction = models.ForeignKey(Faction, related_name='enemies',
                                on_delete=models.PROTECT)
    color = models.ForeignKey(Color, related_name='enemies',
                              on_delete=models.PROTECT)
    damage = models.IntegerField(default=0, blank=False, null=False)
    hp = models.IntegerField(default=0, blank=False, null=False)
    image = models.ImageField(upload_to='enemies/', blank=True, null=True)
    move = models.ForeignKey(Move, related_name='enemies',
                             on_delete=models.PROTECT)
    shield = models.BooleanField(default=False)  # щит, есть или нет, по умолчанию нет
    passive = models.BooleanField(default=False)
    passive_ability = models.ForeignKey(EnemyPassiveAbility, related_name="enemies",
                                        on_delete=models.PROTECT,
                                        blank=True, null=True)
    passive_increase_damage = models.IntegerField(default=0, blank=False, null=False)
    passive_heal = models.IntegerField(default=0, blank=False, null=False)
    passive_heal_leader = models.IntegerField(default=0, blank=False, null=False)
    passive_damage = models.IntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return f'{self.id}:{self.name}, {self.faction}, {self.color}, ' \
               f'damage {self.damage}, hp {self.hp}, move {self.move.name}, shield {self.shield}'


class Level(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False, unique=True)
    starting_enemies_number = models.IntegerField(default=3, blank=False, null=False)  # сколько в начале появляется
    difficulty = models.CharField(choices=LEVEL_DIFFICULTY_CHOICES, blank=False, null=False, max_length=20)
    enemies = models.ManyToManyField(Enemy, through='LevelEnemy', related_name='levels')
    enemy_leader = models.ForeignKey('EnemyLeader', related_name='levels',
                                     on_delete=models.PROTECT,
                                     blank=True, null=True, default=None)

    def __str__(self):
        return f'{self.id}:{self.name}, появление: {self.starting_enemies_number}, ' \
               f'сложность {self.difficulty}, врагов {self.number_of_enemies()}, лидер {self.enemy_leader}'

    def number_of_enemies(self):
        """для админки, чтобы показать это количество"""
        return len(self.l.all())

    class Meta:
        ordering = ('id',)


class LevelEnemy(models.Model):
    level = models.ForeignKey(Level, related_name='l', on_delete=models.CASCADE)
    enemy = models.ForeignKey(Enemy, related_name='l', on_delete=models.CASCADE)


class EnemyLeaderAbility(models.Model):
    """
    damage-once - урон 1 раз
    damage-per-turn - урон каждый ход
    heal-self-per-turn - самолечение каждый ход
    """
    name = models.CharField(max_length=64, blank=False, null=False, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.id} - {self.name}'


class EnemyLeader(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False, unique=True)
    faction = models.ForeignKey(Faction, related_name='enemy_leaders',
                                on_delete=models.PROTECT)
    image = models.ImageField(upload_to='enemy_leaders/', blank=True, null=True)
    passive = models.BooleanField(default=False)
    hp = models.IntegerField(default=0, blank=False, null=False)  # его жизни, должен быть у всех
    ability = models.ForeignKey(EnemyLeaderAbility, related_name='enemy_leaders',
                                on_delete=models.PROTECT,
                                blank=True, null=True, default=None)
    damage_once = models.IntegerField(default=0, blank=True, null=True)  # урон лидера 1 раз
    damage_per_turn = models.IntegerField(default=0, blank=True, null=True)  # урон лидера каждый ход
    heal_self_per_turn = models.IntegerField(default=0, blank=True, null=True)  # самолечение каждый ход

    def __str__(self):
        return f'{self.id} - {self.name}, hp {self.hp}, passive {self.passive}, ' \
               f'абилка - {self.ability.name}, урон {self.damage_once}, ' \
               f'урон/ход {self.damage_per_turn}, heal/turn {self.heal_self_per_turn}'
