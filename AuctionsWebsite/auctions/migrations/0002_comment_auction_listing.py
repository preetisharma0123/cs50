# Generated by Django 4.2 on 2023-06-02 02:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="auction_listing",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments",
                to="auctions.auction_listing",
            ),
        ),
    ]
