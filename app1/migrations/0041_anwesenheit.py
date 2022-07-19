# Generated by Django 3.2.4 on 2022-07-19 15:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0040_auto_20211007_1104'),
    ]

    operations = [
        migrations.CreateModel(
            name='Anwesenheit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datum', models.DateTimeField(auto_now_add=True)),
                ('anwesend', models.BooleanField()),
                ('teilnehmer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.teilnehmer')),
            ],
        ),
    ]