# Generated by Django 5.0.3 on 2024-03-13 07:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0009_listing_current_highest_bid_bid"),
    ]

    operations = [
        migrations.AddField(
            model_name="listing",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
    ]
