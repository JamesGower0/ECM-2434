"""
URL configuration for groupproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from application import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("home/", views.home, name='home'),
    path("register/", views.register, name="register"),
    #path("application/", include("application.urls")),
    path("application/qr/scan/",views.scan,name = "scan"),
    path("application/qr/questions1/", views.questions1, name="questions1"),
    path("application/qr/questions2/", views.questions2, name="questions2"),
    path("qr/questions3/", views.questions3, name="questions3"),
    path("qr/questions4/", views.questions4, name="questions4"),
    path("qr/questions5/", views.questions5, name="questions5"),
    path("application/qr/correct/",views.correct_answer,name = "correct"),
    path("application/qr/wrong/",views.wrong_answer,name="wrong"),
    path("qr/", views.qr, name="qr"),
    path("qr/scan/",views.scan,name = "scan"),
    path("admin/", admin.site.urls),
    path("", views.navBar, name="navBar"),
    path("profile/", views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name = 'login'),
    path('logout/', views.logout_view, name = 'logout'),
    path("leaderboard/", views.leaderboard, name="leaderboard"),
    path("map/", views.map, name="map"),
    path("cookiescript/", views.cookiescript, name="cookiescript"),
    path("cookiepage/",views.cookiepage, name="cookiepage"),
    path("qr/scan/",views.scan,name = "scan"),
    path("qr/questions1/", views.questions1, name="questions1"),
    path("qr/questions2/", views.questions2, name="questions2"),
    path("qr/correct/",views.correct_answer,name = "correct"),
    path("qr/wrong/",views.wrong_answer,name="wrong"),
    path("shop/", views.shop, name="shop"),
]
