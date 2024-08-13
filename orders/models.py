from django.db import models

from products.models import Basket
from users.models import User


class Order(models.Model):
    STATUS_CHOICES = [(0, "Создаётся"), (1, "Оплачен"), (2, "Доставлен")]
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    date = models.DateField().auto_now
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField(default='Россия, Москва, ул. Мира, дом 666')
    basket_history = models.JSONField(default=dict)

    def __str__(self):
        return f'Order #{self.id}'

    def update_after_payment(self):
        baskets = Basket.objects.filter(user=self.user)
        self.status = 1
        self.basket_history = {
            'purchased_items': [basket.de_json() for basket in baskets],
            'total_sum': baskets.total_sum()
        }
        baskets.delete()
        self.save()
