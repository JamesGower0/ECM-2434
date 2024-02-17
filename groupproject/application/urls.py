from django.urls import path

from . import views

urlpatterns = [
    path("", views.qr, name="qr"),
]