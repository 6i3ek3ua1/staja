# Generated by Django 5.0.7 on 2024-08-26 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_remove_order_receipt_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_method_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
