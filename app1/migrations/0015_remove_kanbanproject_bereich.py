# Generated by Django 3.1.1 on 2020-10-28 15:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0014_auto_20201028_1626'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kanbanproject',
            name='bereich',
        ),
    ]
