# Generated by Django 5.0.6 on 2024-06-04 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='ema_rating',
            field=models.FloatField(default=0.0),
        ),
    ]