# Generated by Django 5.0.7 on 2024-08-13 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_basket_history'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[(0, 'Создаётся'), (1, 'Оплачен'), (2, 'Доставлен')], default=0, max_length=50),
        ),
    ]
