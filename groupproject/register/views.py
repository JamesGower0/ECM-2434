from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.http import HttpResponse


# Create your views here.
def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            return redirect("/application/qr/")
            #need to redirect to login page or home page?
    else:
        form = RegisterForm()

    return render(response, "register/register.html", {"form":form})
