from django.urls import path
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    path("", RedirectView.as_view(url="index", permanent=False)),
    path('index', views.index, name='index'),

    path('booking', views.MyBookingView.as_view(), name='booking'),
]
