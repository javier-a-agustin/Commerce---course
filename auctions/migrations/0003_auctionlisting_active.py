# Generated by Django 3.0.8 on 2020-07-31 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auctionlisting_bid_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlisting',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
