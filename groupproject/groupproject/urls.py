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
    #path("profile/changepic/", views.changepic, name="changepic"),
    path("home/", views.home, name='home'),
    path("register/", views.register, name="register"),
    #path("application/", include("application.urls")),
    path("application/qr/scan/",views.scan,name = "scan"),
    path("application/qr/correct/",views.correct_answer,name = "correct"),
    path("application/qr/wrong/",views.wrong_answer,name="wrong"),
    path("admin/", admin.site.urls),
    path("", views.navBar, name="navBar"),
    path("profile/", views.profile, name='profile'),
    path("profile_update/", views.profile_update, name='profile_update'),
    path("change_password/", views.change_password, name='change_password'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name = 'login'),
    path('logout/', views.logout_view, name = 'logout'),
    path("leaderboard/", views.leaderboard, name="leaderboard"),
    path("map/", views.map, name="map"),
    path("cookiescript/", views.cookiescript, name="cookiescript"),
    path("cookiepage/",views.cookiepage, name="cookiepage"),
    path("qr/scan/",views.scan,name = "scan"),
    path("qr/correct/",views.correct_answer,name = "correct"),
    path("qr/wrong/",views.wrong_answer,name="wrong"),
    path("shop/", views.shop, name="shop"),
    path('change-avatar/', views.change_avatar, name='change_avatar'),
    path('add-accessory/', views.add_accessory, name='add_accessory'),
    path("empty_accessories/", views.empty_accessories, name='empty_accessories'),
    path("buy_item/", views.buy_item, name='buy_item'),
    path('profile/<str:username>/', views.user_page, name='user_page'),
    path("location/",views.location, name="location"),
    path("qr/", views.qr, name="qr"),
    path("minigame/",views.minigame,name="minigame"),
    path("minigame/gameover/",views.gameover,name="gameover"),
    path('get-screen-width/', views.get_screen_width, name='get_screen_width')
]
