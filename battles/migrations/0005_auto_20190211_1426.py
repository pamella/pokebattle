# Generated by Django 2.1.6 on 2019-02-11 14:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('battles', '0004_auto_20190211_1255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='battle',
            name='trainer_winner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='battle_winner', to=settings.AUTH_USER_MODEL),
        ),
    ]