from django.db import models


class Faction(models.Model):
    """модель фракции - пока Neutral, Soldiers, Animals, Monsters"""
    name = models.CharField(max_length=32, blank=False, null=False, unique=True)

    def __str__(self):
        return f'{self.id} - {self.name}'


class Color(models.Model):
    """цвет карты - Bronze, Silver, Gold"""
    name = models.CharField(max_length=32, blank=False, null=False, unique=True)

    def __str__(self):
        return f'{self.id} - {self.name}'


class Type(models.Model):
    """тип карты - Unit, Special"""
    name = models.CharField(max_length=32, blank=False, null=False, unique=True)

    def __str__(self):
        return f'{self.id} - {self.name}'


class Ability(models.Model):
    """способность карты"""
    name = models.CharField(max_length=64, blank=False, null=False, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.id} - {self.name}'

    class Meta:
        verbose_name_plural = 'abilities'


class PassiveAbility(models.Model):
    """пассивные способности карт и лидеров"""
    name = models.CharField(max_length=64, blank=False, null=False, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.id} - {self.name}'

    class Meta:
        verbose_name_plural = 'passive abilities'


class Move(models.Model):
    """способность врага ходить: down, stand, random"""
    name = models.CharField(max_length=64, blank=False, null=False, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.id} - {self.name}'


class EnemyPassiveAbility(models.Model):
    """пассивная способность врагов"""
    name = models.CharField(max_length=64, blank=False, null=False, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.id} - {self.name}'

    class Meta:
        verbose_name_plural = 'enemy passive abilities'


class EnemyLeaderAbility(models.Model):
    """способности лидеров врагов"""
    name = models.CharField(max_length=64, blank=False, null=False, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.id} - {self.name}'

    class Meta:
        verbose_name_plural = 'enemy leader abilities'


class GameConst(models.Model):
    """Различные игровые данные"""
    data = models.JSONField()

    def __str__(self):
        return f'{self.data.keys()}'


class Deathwish(models.Model):
    """модель способности завещание у врага"""
    name = models.CharField(max_length=64, blank=False, null=False, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.id} - {self.name}'

    class Meta:
        verbose_name_plural = 'deathwishes'
