from django.conf.urls import url
from . import views
urlpatterns = [
    url('^settlement/$', views.CartListView.as_view()),
    url('^$', views.OrderCreateView.as_view())
]