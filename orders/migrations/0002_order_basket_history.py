# Generated by Django 5.0.7 on 2024-08-11 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='basket_history',
            field=models.JSONField(default=dict),
        ),
    ]
