from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
# Create your views here.

@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def logout_view(request):
    logout(request)
    return render(request, 'logout.html')

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
            return redirect("/login/")
            #need to redirect to login page or home page?
    else:
        form = forms.RegisterForm()

    return render(response, "register.html", {"form":form})