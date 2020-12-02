# Generated by Django 3.1.1 on 2020-10-28 15:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0013_auto_20201027_1559'),
    ]

    operations = [
        migrations.CreateModel(
            name='KanbanBereiche',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('slug', models.CharField(max_length=10, unique=True)),
                ('beschreibung', models.TextField()),
                ('aktiv', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='kanbanproject',
            name='bereich',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app1.kanbanbereiche'),
            preserve_default=False,
        ),
    ]