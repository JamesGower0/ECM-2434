from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def navBar(request):
    return render(request, 'navBar.html')