# Generated by Django 3.1.1 on 2020-12-04 13:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0027_auto_20201203_1218'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ausbildung',
            options={'ordering': ['slug'], 'verbose_name_plural': 'Ausbildungen'},
        ),
        migrations.AlterModelOptions(
            name='fach',
            options={'ordering': ['slug'], 'verbose_name_plural': 'Fächer'},
        ),
        migrations.AlterModelOptions(
            name='gruppe',
            options={'ordering': ['name'], 'verbose_name_plural': 'Gruppen'},
        ),
        migrations.AlterModelOptions(
            name='teilnehmer',
            options={'ordering': ['name'], 'verbose_name_plural': 'Teilnehmer'},
        ),
    ]
