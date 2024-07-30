import json
import uuid
from http import HTTPStatus
from yookassa.domain.notification import WebhookNotificationEventType, WebhookNotificationFactory
from django.http import HttpResponseRedirect, HttpResponse
from yookassa import Configuration, Payment
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.conf import settings
from orders.forms import OrderForm
from products.models import Basket


Configuration.account_id = settings.YOOKASSA_SHOP_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY


class SuccessTemplateView(TemplateView):
    template_name = 'orders/success.html'


class CancelTemplateView(TemplateView):
    template_name = 'orders/cancel.html'


class OrderView(CreateView):
    template_name = 'orders/order-create.html'
    success_url = reverse_lazy('order:order_view')
    form_class = OrderForm

    def post(self, request, *args, **kwargs):
        super(OrderView, self).post(request, *args, **kwargs)
        baskets = Basket.objects.filter(user=self.request.user)
        summ = 0
        for basket in baskets:
            summ += basket.sum()

        payment = Payment.create({
            "amount": {
                "value": f"{summ}",
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "{}{}".format(settings.DOMAIN_NAME, reverse('order:success_order')),
            },
            "capture": True,
            "description": "Заказ №1"
        }, uuid.uuid4())
        return HttpResponseRedirect(payment.confirmation.confirmation_url, status=HTTPStatus.SEE_OTHER)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(OrderView, self).form_valid(form)


@csrf_exempt
def my_webhook_handler(request):
    # Извлечение JSON объекта из тела запроса
    if request.method == 'POST':
        event_json = json.loads(request.body)
        try:
            # Создание объекта класса уведомлений в зависимости от события
            notification_object = WebhookNotificationFactory().create(event_json)
            response_object = notification_object.object
            if notification_object.event == WebhookNotificationEventType.PAYMENT_SUCCEEDED:
                some_data = {
                    'paymentId': response_object.id,
                    'paymentStatus': response_object.status,
                }
                # Специфичная логика
                # ...
            elif notification_object.event == WebhookNotificationEventType.PAYMENT_WAITING_FOR_CAPTURE:
                some_data = {
                    'paymentId': response_object.id,
                    'paymentStatus': response_object.status,
                }
                # Специфичная логика
                # ...
            elif notification_object.event == WebhookNotificationEventType.PAYMENT_CANCELED:
                some_data = {
                    'paymentId': response_object.id,
                    'paymentStatus': response_object.status,
                }
                # Специфичная логика
                # ...
            elif notification_object.event == WebhookNotificationEventType.REFUND_SUCCEEDED:
                some_data = {
                    'refundId': response_object.id,
                    'refundStatus': response_object.status,
                    'paymentId': response_object.payment_id,
                }
                # Специфичная логика
                # ...
            elif notification_object.event == WebhookNotificationEventType.DEAL_CLOSED:
                some_data = {
                    'dealId': response_object.id,
                    'dealStatus': response_object.status,
                }
                # Специфичная логика
                # ...
            elif notification_object.event == WebhookNotificationEventType.PAYOUT_SUCCEEDED:
                some_data = {
                    'payoutId': response_object.id,
                    'payoutStatus': response_object.status,
                    'dealId': response_object.deal.id,
                }
                # Специфичная логика
                # ...
            elif notification_object.event == WebhookNotificationEventType.PAYOUT_CANCELED:
                some_data = {
                    'payoutId': response_object.id,
                    'payoutStatus': response_object.status,
                    'dealId': response_object.deal.id,
                }
                # Специфичная логика
                # ...
            else:
                # Обработка ошибок
                print('ultrabruh')
                return HttpResponse(status=400)  # Сообщаем кассе об ошибке

            # Специфичная логика
            # ...
            Configuration.configure(settings.YOOKASSA_SHOP_ID, settings.YOOKASSA_SECRET_KEY)
            # Получим актуальную информацию о платеже
            payment_info = Payment.find_one(some_data['paymentId'])
            if payment_info:
                payment_status = payment_info.status
                # Специфичная логика
                # ...
                print('emae')
                print(some_data, event_json)
            else:
                # Обработка ошибок
                print('bruh')
                return HttpResponse(status=400)  # Сообщаем кассе об ошибке

        except Exception as e:
            # Обработка ошибок
            print('megabruh', str(e))
            return HttpResponse(status=400)  # Сообщаем кассе об ошибке

        return HttpResponse(status=200)  # Сообщаем кассе, что все хорошо
