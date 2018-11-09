from django.conf.urls import url
from . import views

urlpatterns = [
        url('^orders/(?P<order_id>\d+)/payment/$', views.AliPayURLView.as_view()),
        url('^payment/status/$', views.OrderStatusView.as_view())
]
