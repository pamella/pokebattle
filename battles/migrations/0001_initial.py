# Generated by Django 2.1.5 on 2019-02-08 13:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pokemons', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Battle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(default='def', max_length=56)),
                ('trainer_creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='battle_creator', to=settings.AUTH_USER_MODEL)),
                ('trainer_opponent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='battle_opponent', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TrainerTeam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('battle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='battles.Battle')),
                ('pokemons', models.ManyToManyField(to='pokemons.Pokemon')),
                ('trainer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]