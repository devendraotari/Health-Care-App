# Generated by Django 2.2.10 on 2020-10-05 14:49

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeSlot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(default=datetime.datetime(2020, 10, 5, 14, 49, 31, 1039))),
                ('is_booked', models.BooleanField(default=False, verbose_name='is_booked')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='available_slot', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(default='created', max_length=50)),
                ('booked_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointment', to=settings.AUTH_USER_MODEL)),
                ('booking_slot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointment', to='appointment.TimeSlot')),
            ],
        ),
    ]
