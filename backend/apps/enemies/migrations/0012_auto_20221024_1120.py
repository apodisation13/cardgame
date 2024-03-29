# Generated by Django 3.2.8 on 2022-10-24 11:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('enemies', '0011_alter_level_related_levels'),
    ]

    operations = [
        migrations.AlterField(
            model_name='levelrelatedlevels',
            name='level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='children', to='enemies.level'),
        ),
        migrations.AlterField(
            model_name='levelrelatedlevels',
            name='line',
            field=models.CharField(blank=True, choices=[('down', 'down'), ('up', 'up'), ('right', 'right'), ('left', 'left'), (None, None)], max_length=16, null=True),
        ),
    ]
