# Generated by Django 3.2.8 on 2022-11-29 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0003_auto_20221016_0838'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='default_timer',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='card',
            name='reset_timer',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='card',
            name='value',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='leader',
            name='default_timer',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='leader',
            name='reset_timer',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='leader',
            name='timer',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='leader',
            name='value',
            field=models.IntegerField(default=0),
        ),
    ]
