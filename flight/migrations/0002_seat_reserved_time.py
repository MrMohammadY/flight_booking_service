# Generated by Django 3.2 on 2022-01-26 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='seat',
            name='reserved_time',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]
