"""
Defines URL patterns for the application

Author: 
"""
from django.urls import path
from . import views

urlpatterns = [
    path("qr/questions", views.qr, name="qr"),
    path("qr/scan/",views.scan,name = "scan"),
    path("qr/correct/",views.correct_answer,name = "correct"),
    path("qr/wrong/",views.wrong_answer,name="wrong"),
    path("home/", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("leaderboard/", views.leaderboard, name="leaderboard"),
    path("navBar/", views.navBar, name="navBar"),
    path("map/", views.map, name="map"),
    path("cookiescript/", views.cookiescript, name="cookiescript"),
    path("cookiepage/",views.cookiepage, name="cookiepage"),
]
