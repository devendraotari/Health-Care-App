# Generated by Django 2.2.10 on 2020-09-06 12:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("consultation", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="patientprofile",
            name="patient",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="patient",
                to=settings.AUTH_USER_MODEL,
                verbose_name="customUser",
            ),
        ),
        migrations.AddField(
            model_name="generalsymptom",
            name="assigned_doctor",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="assigned_doctor",
                to=settings.AUTH_USER_MODEL,
                verbose_name="doctor",
            ),
        ),
        migrations.AddField(
            model_name="generalsymptom",
            name="patient",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="from_patient",
                to=settings.AUTH_USER_MODEL,
                verbose_name="patient",
            ),
        ),
        migrations.AddField(
            model_name="doctorprofile",
            name="doctor",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="doctor",
                to=settings.AUTH_USER_MODEL,
                verbose_name="customUser",
            ),
        ),
        migrations.AddField(
            model_name="doctorprofile",
            name="patients",
            field=models.ManyToManyField(
                related_name="patients",
                to=settings.AUTH_USER_MODEL,
                verbose_name="patients",
            ),
        ),
        migrations.AddField(
            model_name="doctorprofile",
            name="qualification",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="consultation.Qualification",
                verbose_name="qualification",
            ),
        ),
    ]
