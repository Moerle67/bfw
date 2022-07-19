# Generated by Django 3.2.4 on 2021-10-07 11:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0039_alter_ausbilder_aktiv'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='gruppe',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app1.gruppe'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='planzeiten',
            name='einheit',
            field=models.IntegerField(unique=True),
        ),
    ]