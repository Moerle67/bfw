# Generated by Django 3.1.1 on 2020-10-26 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0008_auto_20201026_1033'),
    ]

    operations = [
        migrations.AddField(
            model_name='teilnehmer',
            name='vorname',
            field=models.CharField(default='Leer', max_length=50),
            preserve_default=False,
        ),
    ]