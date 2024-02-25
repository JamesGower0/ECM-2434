from django.urls import path
from . import views

urlpatterns = [
    path("qr/", views.qr, name="qr"),
    path("home/", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("leaderboard/", views.leaderboard, name="leaderboard"),
    path("navBar/", views.navBar, name="navBar"),
]