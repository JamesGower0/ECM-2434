from django.urls import path
from navBar import views as nbv
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("", nbv.navBar, name="navBar")
]