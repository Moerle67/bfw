# Generated by Django 3.1.1 on 2020-11-22 12:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0018_kanbanprotokoll'),
    ]

    operations = [
        migrations.AddField(
            model_name='teilnehmer',
            name='gruppe',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.gruppe'),
        ),
        migrations.DeleteModel(
            name='gruppeTN',
        ),
    ]
