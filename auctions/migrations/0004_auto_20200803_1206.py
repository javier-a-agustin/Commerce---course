# Generated by Django 3.0.8 on 2020-08-03 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auctionlisting_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='imgUrl',
            field=models.URLField(),
        ),
    ]
