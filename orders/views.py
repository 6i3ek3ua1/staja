import json
import time
import uuid
from http import HTTPStatus
from django.views.generic import ListView
from yookassa.domain.notification import WebhookNotificationEventType, WebhookNotificationFactory
from django.http import HttpResponseRedirect, HttpResponse
from yookassa import Configuration, Payment, Receipt
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.conf import settings
from orders.forms import OrderForm
from products.models import Basket
from orders.models import Order
from orders.tasks import initiate_auto_payments


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
        orders = Order.objects.filter(user=self.request.user)
        last_order = orders.last()
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
            "description": f"{last_order.id}"
        }, uuid.uuid4())
        return HttpResponseRedirect(payment.confirmation.confirmation_url, status=HTTPStatus.SEE_OTHER)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(OrderView, self).form_valid(form)


class OrderConsultView(CreateView):
    template_name = 'orders/order-auto.html'
    success_url = reverse_lazy('order:order_consult')
    form_class = OrderForm

    def post(self, request, *args, **kwargs):
        super(OrderConsultView, self).post(request, *args, **kwargs)
        orders = Order.objects.filter(user=self.request.user)
        last_order = orders.last()
        payment = Payment.create({
            "amount": {
                "value": "50.00",
                "currency": "RUB"
            },
            "payment_method_data": {
                "type": "bank_card"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "{}{}".format(settings.DOMAIN_NAME, reverse('order:success_order'))
            },
            "capture": True,
            "description": f"{last_order.id}",
            "save_payment_method": True
        }, uuid.uuid4())
        result = initiate_auto_payments.delay()
        print(result)
        return HttpResponseRedirect(payment.confirmation.confirmation_url, status=HTTPStatus.SEE_OTHER)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(OrderConsultView, self).form_valid(form)


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
                    'orderId': int(response_object.description),
                }

            elif notification_object.event == WebhookNotificationEventType.PAYMENT_WAITING_FOR_CAPTURE:
                some_data = {
                    'paymentId': response_object.id,
                    'paymentStatus': response_object.status,
                }

            elif notification_object.event == WebhookNotificationEventType.PAYMENT_CANCELED:
                some_data = {
                    'paymentId': response_object.id,
                    'paymentStatus': response_object.status,
                }

            elif notification_object.event == WebhookNotificationEventType.REFUND_SUCCEEDED:
                some_data = {
                    'refundId': response_object.id,
                    'refundStatus': response_object.status,
                    'paymentId': response_object.payment_id,
                }

            elif notification_object.event == WebhookNotificationEventType.DEAL_CLOSED:
                some_data = {
                    'dealId': response_object.id,
                    'dealStatus': response_object.status,
                }

            elif notification_object.event == WebhookNotificationEventType.PAYOUT_SUCCEEDED:
                some_data = {
                    'payoutId': response_object.id,
                    'payoutStatus': response_object.status,
                    'dealId': response_object.deal.id,
                }

            elif notification_object.event == WebhookNotificationEventType.PAYOUT_CANCELED:
                some_data = {
                    'payoutId': response_object.id,
                    'payoutStatus': response_object.status,
                    'dealId': response_object.deal.id,
                }
            else:
                # Обработка ошибок
                print('ultrabruh')
                return HttpResponse(status=400)  # Сообщаем кассе об ошибке


            Configuration.configure(settings.YOOKASSA_SHOP_ID, settings.YOOKASSA_SECRET_KEY)
            # Получим актуальную информацию о платеже
            payment_info = Payment.find_one(some_data['paymentId'])
            if payment_info:
                payment_status = payment_info.status
                if payment_status == "succeeded":
                    if payment_info.payment_method.saved:
                        order_id = some_data['orderId']
                        order = Order.objects.get(id=order_id)
                        order.add_payment_id(payment_info.payment_method.id)
                        print('autoklass')
                    else:
                        order_id = some_data['orderId']
                        order = Order.objects.get(id=order_id)
                        order.update_after_payment()
                        print('emae_klass')
                else:
                    print('emae ne klass')

            else:
                # Обработка ошибок
                print('bruh')
                return HttpResponse(status=400)  # Сообщаем кассе об ошибке

        except Exception as e:
            # Обработка ошибок
            print('megabruh', str(e))
            return HttpResponse(status=400)  # Сообщаем кассе об ошибке

        return HttpResponse(status=200)  # Сообщаем кассе, что все хорошо


class OrderListView(ListView):
    template_name = 'orders/order-list.html'
    title = 'Мои заказы'
    queryset = Order.objects.all()

    def get_queryset(self):
        queryset = super(OrderListView, self).get_queryset()
        return queryset.filter(user=self.request.user)
