# Generated by Django 5.0.3 on 2024-03-30 23:00

import django.db.models.manager
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("languages", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="language",
            managers=[
                ("language_manager", django.db.models.manager.Manager()),
            ],
        ),
    ]