# Generated by Django 3.2.4 on 2021-06-23 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0035_auto_20210330_1119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teilnehmer',
            name='email',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='teilnehmer',
            name='mobil',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
