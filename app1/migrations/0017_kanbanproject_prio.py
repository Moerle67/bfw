# Generated by Django 3.1.3 on 2020-11-15 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0016_kanbanproject_bereich'),
    ]

    operations = [
        migrations.AddField(
            model_name='kanbanproject',
            name='prio',
            field=models.IntegerField(default=5),
            preserve_default=False,
        ),
    ]