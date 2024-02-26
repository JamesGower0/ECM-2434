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
    #path("application/qr/", include("application.urls")),
    path("admin/", admin.site.urls),
    path("map/", views.map, name="map"),
    path("", views.navBar, name="navBar"),
    path("profile/", views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name = 'login'),
    path('logout/', views.logout_view, name = 'logout'),
    path('leaderboard/', views.leaderboard, name = 'leaderboard'),
]
