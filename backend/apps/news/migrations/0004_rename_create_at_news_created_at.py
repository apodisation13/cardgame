# Generated by Django 3.2.8 on 2022-08-24 14:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_alter_news_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='news',
            old_name='create_at',
            new_name='created_at',
        ),
    ]
