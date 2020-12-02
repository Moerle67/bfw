# Generated by Django 3.1.1 on 2020-11-20 21:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0017_kanbanproject_prio'),
    ]

    operations = [
        migrations.CreateModel(
            name='KanbanProtokoll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kommentar', models.TextField()),
                ('stufeNeu', models.IntegerField()),
                ('zeitpunkt', models.TimeField(auto_now_add=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.kanbanproject')),
            ],
        ),
    ]
