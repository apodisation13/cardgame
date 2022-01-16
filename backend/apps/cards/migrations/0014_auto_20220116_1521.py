# Generated by Django 3.2.8 on 2022-01-16 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0013_deck_leader'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='leader',
            name='passive',
            field=models.BooleanField(default=False),
        ),
    ]