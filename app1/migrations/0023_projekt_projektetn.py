# Generated by Django 3.1.1 on 2020-12-03 10:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app1', '0022_tninfo_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Projekt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bezeichnung', models.CharField(max_length=100)),
                ('start', models.DateTimeField(auto_now_add=True)),
                ('fach', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.fach')),
                ('gruppe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.gruppe')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProjekteTN',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bis', models.DateTimeField()),
                ('abgabe', models.DateTimeField(default=None)),
                ('bewertung', models.IntegerField(default=0)),
                ('kommentar', models.CharField(default='', max_length=100)),
                ('projekt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.projekt')),
                ('teilnehmer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.teilnehmer')),
            ],
        ),
    ]
