# Generated by Django 3.1.1 on 2021-03-29 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0031_mitarbeit_mitarbeit_thema'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mitarbeit',
            name='thema_erledigt',
        ),
        migrations.AddField(
            model_name='mitarbeit',
            name='tn_ok',
            field=models.BooleanField(default=False),
        ),
    ]