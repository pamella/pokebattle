# Generated by Django 2.1.7 on 2019-03-27 13:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('battles', '0010_auto_20190325_1105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainerteam',
            name='battle_related',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teams', to='battles.Battle'),
        ),
    ]
