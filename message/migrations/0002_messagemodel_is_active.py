# Generated by Django 2.2.5 on 2019-10-30 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='messagemodel',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
