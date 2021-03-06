# Generated by Django 2.2.10 on 2020-09-13 15:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('consultation', '0003_auto_20200913_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qualification',
            name='doctor_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctor_qualification', to='consultation.DoctorProfile', verbose_name='doctor_profile'),
        ),
    ]
