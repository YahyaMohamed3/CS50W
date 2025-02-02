# Generated by Django 5.1.1 on 2024-09-29 05:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Listing",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=64)),
                ("details", models.TextField()),
                ("starting_bid", models.IntegerField()),
                ("picture", models.URLField(blank=True, null=True)),
                (
                    "category",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Electronics", "Electronics"),
                            ("Furniture", "Furniture"),
                            ("Clothing", "Clothing"),
                            ("Other", "Other"),
                        ],
                        max_length=32,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="listings",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
