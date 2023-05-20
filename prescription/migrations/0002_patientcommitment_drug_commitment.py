# Generated by Django 4.1.2 on 2023-05-13 13:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_initial'),
        ('prescription', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PatientCommitment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('status', models.BooleanField()),
                ('drug', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prescription.drug')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.patient')),
            ],
        ),
        migrations.AddField(
            model_name='drug',
            name='commitment',
            field=models.ManyToManyField(through='prescription.PatientCommitment', to='accounts.patient'),
        ),
    ]