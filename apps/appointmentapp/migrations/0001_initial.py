# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-08-20 03:21
from __future__ import unicode_literals

import apps.appointmentapp.models
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('status', models.IntegerField(choices=[(1, 'Done'), (2, 'Pending'), (3, 'Missed')], default=2)),
                ('date', models.DateField(validators=[apps.appointmentapp.models.validate_future_date])),
                ('time', models.TimeField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
            ],
            managers=[
                ('taskMgr', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('date_of_birth', models.DateField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
            ],
            managers=[
                ('Usermgr', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itemcreater', to='appointmentapp.User'),
        ),
    ]
