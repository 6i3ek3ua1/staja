from django.urls import path
from .views import OrderView, SuccessTemplateView, CancelTemplateView, OrderListView, OrderConsultView #, AutoPayment

app_name = 'order'
urlpatterns = [
    path('', OrderView.as_view(), name='order_view'),
    path('success/', SuccessTemplateView.as_view(), name='success_order'),
    path('canсel/', CancelTemplateView.as_view(), name='cancel_order'),
    path('list/', OrderListView.as_view(), name='list_order'),
    path('consult/', OrderConsultView.as_view(), name='order_consult'),
    '''path('consult/auto/', AutoPayment.as_view(), name='auto_order_consult'),'''
]
