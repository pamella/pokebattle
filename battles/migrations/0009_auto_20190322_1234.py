# Generated by Django 2.1.7 on 2019-03-22 12:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('battles', '0008_invite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='battle',
            name='trainer_creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='battles_creator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='battle',
            name='trainer_opponent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='battles_opponent', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='battle',
            name='trainer_winner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='trainerteam',
            name='trainer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teams', to=settings.AUTH_USER_MODEL),
        ),
    ]
