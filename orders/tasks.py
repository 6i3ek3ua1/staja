import uuid
from http import HTTPStatus

from celery import shared_task
from django.http import HttpResponseRedirect
from yookassa import Payment, Configuration
from staja import settings
from .models import Order


Configuration.account_id = settings.YOOKASSA_SHOP_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY


@shared_task
def initiate_auto_payments():
    orders = Order.objects.filter(is_active=True)
    print(orders)

    for payment in orders:
        try:
            new_payment = Payment.create({
                "amount": {
                    "value": "150.00",
                    "currency": "RUB"
                },
                "payment_method_data": {
                    "type": "bank_card"
                },
                "capture": True,
                "payment_method_id": payment.payment_id,
                "description": f"{payment.id}",
                "save_payment_method": True
            }, uuid.uuid4())
            print("OKKKK")
            return HttpResponseRedirect(new_payment.confirmation.confirmation_url, status=HTTPStatus.SEE_OTHER)
        except Exception as e:
            # Логирование ошибки или уведомление администратора
            print(f"Error processing auto payment {payment.id}: {str(e)}")
