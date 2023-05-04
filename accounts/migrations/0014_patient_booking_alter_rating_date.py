# Generated by Django 4.1.2 on 2023-05-01 01:17

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('prescription', '0014_delete_patientbooking'),
        ('accounts', '0013_alter_rating_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='booking',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='prescription.booking'),
        ),
        migrations.AlterField(
            model_name='rating',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
