# Generated by Django 3.1.6 on 2021-03-15 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flowcode', '0003_auto_20210305_1147'),
    ]

    operations = [
        migrations.CreateModel(
            name='VizQuery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
            ],
        ),
    ]
