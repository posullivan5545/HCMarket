# Generated by Django 5.1 on 2024-12-03 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HCMarket', '0003_product_image_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='in_negotiation',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='is_sold',
            field=models.BooleanField(default=False),
        ),
    ]
