# Generated by Django 3.2.8 on 2022-11-29 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0004_auto_20221129_1043'),
    ]

    operations = [
        migrations.AddField(
            model_name='leader',
            name='heal',
            field=models.IntegerField(default=0),
        ),
    ]
