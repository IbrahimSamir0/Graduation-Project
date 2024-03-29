# Generated by Django 4.1.2 on 2023-05-11 14:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='contactModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='your email')),
                ('text', models.TextField(max_length=1000, verbose_name='How can we help you?')),
                ('image', models.TextField(null=True)),
                ('date', models.DateField(default=datetime.datetime.now)),
            ],
        ),
    ]
