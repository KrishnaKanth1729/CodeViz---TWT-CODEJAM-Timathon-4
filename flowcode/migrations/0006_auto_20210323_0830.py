# Generated by Django 3.1.6 on 2021-03-23 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flowcode', '0005_candle'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='candle',
            name='end',
        ),
        migrations.RemoveField(
            model_name='candle',
            name='start',
        ),
        migrations.AlterField(
            model_name='candle',
            name='ticker',
            field=models.CharField(default='AAPL', max_length=255),
        ),
    ]
