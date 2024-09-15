import time
import uuid
import schedule
from celery import shared_task, Celery
from yookassa import Payment, Configuration
from staja import settings
from .models import Order


Configuration.account_id = settings.YOOKASSA_SHOP_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY

app = Celery('tasks', broker='redis://localhost:6379/0')


@shared_task
def initiate_auto_payments(id):
    schedule.every(30).seconds.do(auto_payments, id)

    while True:
        schedule.run_pending()
        time.sleep(1)


def auto_payments(id):
    orders = Order.objects.filter(id=id)

    for payment in orders:
        try:
            new_payment = Payment.create({
                "amount": {
                    "value": "150.00",
                    "currency": "RUB"
                },
                "capture": True,
                "payment_method_id": payment.payment_id,
                "description": f"{payment.id}",
                "receipt": {
                    "customer": {
                        "email": "slyantyaev20@yandex.ru",
                    },
                    "items": [
                        {
                            "description": "Подписка",
                            "quantity": 1.000,
                            "amount": {
                                "value": "150.00",
                                "currency": "RUB"
                            },
                            "vat_code": 2,
                            "payment_mode": "full_payment",
                            "payment_subject": "commodity",
                            "country_of_origin_code": "CN"
                        },
                    ]
                }
            }, uuid.uuid4())
            return 'OKKKKKKK'
        except Exception as e:
            # Логирование ошибки или уведомление администратора
            print(f"Error processing auto payment {payment.id}: {str(e)}")
