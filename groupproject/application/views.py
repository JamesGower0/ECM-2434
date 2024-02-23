from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import forms

# Create your views here.

def qr(request):
    return HttpResponse("placeholder for qr functionality")

def navBar(request):
    return render(request, 'navBar.html')

def home(request):
    template = "home.html"
    context = {}
    return render(request, "home.html", context)

def register(response):
    if response.method == "POST":
        form = forms.RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            return redirect("/home/")
            #need to redirect to login page or home page?
    else:
        form = forms.RegisterForm()

    return render(response, "register.html", {"form":form})

def map(request):
    return render(request, "map.html")