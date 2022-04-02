# Generated by Django 3.2.8 on 2022-04-01 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0002_auto_20220401_1521'),
    ]

    operations = [
        migrations.CreateModel(
            name='PassiveAbility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
