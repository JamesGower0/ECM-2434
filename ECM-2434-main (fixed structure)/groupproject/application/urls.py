from django.urls import path
from . import views

urlpatterns = [
    path("qr/", views.qr, name="qr"),
    path("home/", views.home, name="home"),
    path("navBar/", views.navBar, name="navBar"),
    path("register/", views.register, name="register"),
]