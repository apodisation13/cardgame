# Generated by Django 3.2.8 on 2022-02-11 13:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cards', '0019_alter_card_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Enemy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('damage', models.IntegerField(default=0)),
                ('hp', models.IntegerField(default=0)),
                ('image', models.ImageField(blank=True, null=True, upload_to='enemies/')),
                ('shield', models.BooleanField(default=False)),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='enemies', to='cards.color')),
                ('faction', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='enemies', to='cards.faction')),
            ],
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('starting_enemies_number', models.IntegerField(default=3)),
                ('difficulty', models.CharField(choices=[('easy', 'easy'), ('normal', 'normal'), ('hard', 'hard')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Move',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='LevelEnemy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enemy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='l', to='enemies.enemy')),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='l', to='enemies.level')),
            ],
        ),
        migrations.AddField(
            model_name='level',
            name='enemies',
            field=models.ManyToManyField(related_name='levels', through='enemies.LevelEnemy', to='enemies.Enemy'),
        ),
        migrations.AddField(
            model_name='enemy',
            name='move',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='enemies', to='enemies.move'),
        ),
    ]