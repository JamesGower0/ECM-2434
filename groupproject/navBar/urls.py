from django.urls import path
from . import views
from home import views as hv
from register import views as rv
from application import views as av



urlpatterns = [
    path("", views.navBar, name="navBar"),
    path("", hv.home, name="home"),
    path("", rv.register, name="register"),
    #path("", av.application, name="application"),
]