from django.db import models

from apps.accounts.models import CustomUser
from apps.core.models import Color, Deathwish, EnemyLeaderAbility, EnemyPassiveAbility, Faction, Move

LEVEL_DIFFICULTY_CHOICES = (
    ('easy', 'easy'),
    ('normal', 'normal'),
    ('hard', 'hard'),
)

LINE_CHOICES = (
    ("down", "down"),
    ("up", "up"),
    ("right", "right"),
    ("left", "left"),
    (None, None),
)


class Enemy(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False, unique=True)
    faction = models.ForeignKey(Faction, related_name='enemies',
                                on_delete=models.PROTECT)
    color = models.ForeignKey(Color, related_name='enemies',
                              on_delete=models.PROTECT)
    damage = models.IntegerField(default=0, blank=False, null=False)
    hp = models.IntegerField(default=0, blank=False, null=False)
    base_hp = models.IntegerField(default=0, blank=False, null=False)
    image = models.ImageField(upload_to='enemies/', blank=True, null=True)
    move = models.ForeignKey(Move, related_name='enemies',
                             on_delete=models.PROTECT)
    shield = models.BooleanField(default=False)  # щит, есть или нет, по умолчанию нет
    has_passive = models.BooleanField(default=False)
    has_passive_in_field = models.BooleanField(default=False)
    has_passive_in_deck = models.BooleanField(default=False)
    has_passive_in_grave = models.BooleanField(default=False)
    passive_ability = models.ForeignKey(EnemyPassiveAbility, related_name="enemies",
                                        on_delete=models.PROTECT,
                                        blank=True, null=True)
    value = models.IntegerField(default=0, blank=False, null=False)
    timer = models.IntegerField(default=0, blank=False, null=False)
    default_timer = models.IntegerField(default=0, blank=False, null=False)
    reset_timer = models.BooleanField(default=False)
    each_tick = models.BooleanField(default=False)
    has_deathwish = models.BooleanField(default=False)
    deathwish = models.ForeignKey(Deathwish, related_name='enemies',
                                  on_delete=models.PROTECT,
                                  blank=True, null=True)
    deathwish_value = models.IntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return f'{self.id}:{self.name}, {self.faction}, {self.color}, ' \
               f'damage {self.damage}, hp {self.hp}, move {self.move.name}, shield {self.shield}'

    class Meta:
        verbose_name_plural = 'enemies'


class EnemyLeader(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False, unique=True)
    faction = models.ForeignKey(Faction, related_name='enemy_leaders',
                                on_delete=models.PROTECT)
    image = models.ImageField(upload_to='enemy_leaders/', blank=True, null=True)
    has_passive = models.BooleanField(default=False)
    hp = models.IntegerField(default=0, blank=False, null=False)  # его жизни, должен быть у всех
    base_hp = models.IntegerField(default=0, blank=False, null=False)
    ability = models.ForeignKey(EnemyLeaderAbility, related_name='enemy_leaders',
                                on_delete=models.PROTECT,
                                blank=True, null=True, default=None)
    passive_ability = models.ForeignKey(EnemyPassiveAbility, related_name="enemy_leaders",
                                        on_delete=models.PROTECT,
                                        blank=True, null=True)
    value = models.IntegerField(default=0, blank=False, null=False)
    timer = models.IntegerField(default=0, blank=False, null=False)
    default_timer = models.IntegerField(default=0, blank=False, null=False)
    reset_timer = models.BooleanField(default=False)
    each_tick = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.id} - {self.name}, hp {self.hp}, passive {self.has_passive}, ' \
               f'абилка - {self.ability.name}, пассивка - {self.passive_ability}'


class Level(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False, unique=True)
    starting_enemies_number = models.IntegerField(default=3,
                                                  blank=False, null=False)  # сколько в начале появляется
    difficulty = models.CharField(choices=LEVEL_DIFFICULTY_CHOICES,
                                  blank=False, null=False, max_length=20)
    enemies = models.ManyToManyField(Enemy,
                                     related_name='levels',
                                     through='LevelEnemy')
    enemy_leader = models.ForeignKey('EnemyLeader', related_name='levels',
                                     on_delete=models.PROTECT,
                                     blank=True, null=True, default=None)
    unlocked = models.BooleanField(default=False)
    related_levels = models.ManyToManyField("Level", through="LevelRelatedLevels", related_name="rel_levels")
    season = models.ForeignKey("Season",
                               on_delete=models.CASCADE,
                               related_name="levels",
                               blank=True, null=True)
    x = models.IntegerField(default=0)  # координаты уровня в дереве на экране
    y = models.IntegerField(default=0)  # координаты уровня в дереве на экране

    def __str__(self):
        return f'{self.id}:{self.name}, появление: {self.starting_enemies_number}, ' \
               f'сложность {self.difficulty}, врагов {self.number_of_enemies()}, лидер {self.enemy_leader}'

    def number_of_enemies(self):
        """для админки, чтобы показать это количество"""
        return len(self.l.all())

    def get_related_levels(self):
        """для админки, чтобы показать краткую информацию"""
        return [(level.id, level.name) for level in self.related_levels.all()]

    class Meta:
        ordering = ('id',)


class LevelRelatedLevels(models.Model):
    level = models.ForeignKey(Level, related_name="children", on_delete=models.CASCADE)
    related_level = models.ForeignKey(Level, related_name="l2", on_delete=models.CASCADE)
    line = models.CharField(choices=LINE_CHOICES, blank=True, null=True, max_length=16)
    connection = models.CharField(max_length=16, blank=False, null=False)

    def save(self, *args, **kwargs):
        self.connection = f"{self.level_id}-{self.related_level_id}"
        return super(LevelRelatedLevels, self).save(*args, **kwargs)

    class Meta:
        unique_together = ("level", "related_level")


class LevelEnemy(models.Model):
    level = models.ForeignKey(Level, related_name='l', on_delete=models.CASCADE)
    enemy = models.ForeignKey(Enemy, related_name='l', on_delete=models.CASCADE)


class UserLevel(models.Model):
    level = models.ForeignKey(Level, related_name="u_level",
                              on_delete=models.CASCADE,
                              blank=False, null=False)
    user = models.ForeignKey(CustomUser, related_name="u_level",
                             on_delete=models.CASCADE,
                             blank=False, null=False)
    finished = models.BooleanField(default=False)


class Season(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False)
    description = models.TextField(blank=False, null=False)

    def __str__(self):
        return f"{self.name}, {self.description[:30]}"
