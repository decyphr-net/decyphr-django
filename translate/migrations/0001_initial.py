# Generated by Django 5.0.3 on 2024-03-29 18:04

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Translation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("source_text", models.TextField()),
                ("translated_text", models.TextField()),
            ],
        ),
    ]
