# Generated by Django 2.1.7 on 2019-03-08 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemons', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemon',
            name='api_id',
            field=models.SmallIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pokemon',
            name='sprite',
            field=models.URLField(default='1'),
            preserve_default=False,
        ),
    ]
