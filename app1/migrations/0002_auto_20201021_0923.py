# Generated by Django 3.1.1 on 2020-10-21 07:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gruppetn',
            old_name='Teilnehmer',
            new_name='teilnehmer',
        ),
    ]
