# Generated by Django 3.1.1 on 2020-10-28 15:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0015_remove_kanbanproject_bereich'),
    ]

    operations = [
        migrations.AddField(
            model_name='kanbanproject',
            name='bereich',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='app1.kanbanbereiche'),
            preserve_default=False,
        ),
    ]
