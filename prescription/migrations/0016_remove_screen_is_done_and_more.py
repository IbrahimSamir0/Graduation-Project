# Generated by Django 4.1.2 on 2023-05-04 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prescription', '0015_patientbooking'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='screen',
            name='is_done',
        ),
        migrations.AlterField(
            model_name='active_ingredient',
            name='if_interaction_exist',
            field=models.BooleanField(default=None),
        ),
    ]
