# Generated by Django 3.1.1 on 2021-03-30 11:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0033_mitarbeit_gruppe'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teilnehmer',
            name='gruppe',
        ),
    ]
