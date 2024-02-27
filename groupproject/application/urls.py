from django.urls import path
from . import views

urlpatterns = [
    path("qr/", views.qr, name="qr"),
    path("qr/scan/",views.scan,name = "scan"),
    path("qr/questions1/", views.questions1, name="questions1"),
    path("qr/questions2/", views.questions2, name="questions2"),
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
