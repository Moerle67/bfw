# Generated by Django 4.1.6 on 2024-01-16 15:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0044_delete_add_gruppe_sprecher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gruppe',
            name='raum',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.raum'),
        ),
    ]
