"""
Defines URL patterns for the application

Author: 
"""
from django.urls import path
from . import views

urlpatterns = [
    path("qr/", views.qr, name="qr"),
    path("qr/scan/",views.scan,name = "scan"),
    path("qr/questions1/", views.questions1, name="questions1"),
    path("qr/questions2/", views.questions2, name="questions2"),
    path("qr/questions3/", views.questions3, name="questions3"),
    path("qr/questions4/", views.questions4, name="questions4"),
    path("qr/questions5/", views.questions5, name="questions5"),
    path("qr/correct/",views.correct_answer,name = "correct"),
    path("qr/wrong/",views.wrong_answer,name="wrong"),
    path("home/", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("leaderboard/", views.leaderboard, name="leaderboard"),
    path("navBar/", views.navBar, name="navBar"),
    path("map/", views.map, name="map"),
    path("cookiescript/", views.cookiescript, name="cookiescript"),
    path("cookiepage/",views.cookiepage, name="cookiepage"),
    path("shop/", views.shop, name="shop"),
    path('change-avatar/', views.change_avatar, name='change_avatar'),
    path('add-accessory/', views.add_accessory, name='add_accessory'),
    path("location/",views.location, name="location"),
    path("gameover/",views.gameover,name="gameover"),
]
