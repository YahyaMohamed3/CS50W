# Generated by Django 5.1.1 on 2024-09-30 01:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0006_bid"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Comment",
        ),
    ]
