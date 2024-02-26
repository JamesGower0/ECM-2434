from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Score, Quiz
# Create your views here.

@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def logout_view(request):
    logout(request)
    return render(request, 'home.html')

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
            user = form.save(commit=False)
            user.avatar_choice = form.cleaned_data['avatar_choice']
            print("Avatar Choice:", user.avatar_choice)
            user.save()
            return redirect("/login/")
            #need to redirect to login page or home page?
    else:
        form = forms.RegisterForm()

    return render(response, "register.html", {"form":form})

def map(request):
    return render(request, "map.html")

def leaderboard(request):
    quizzes = Quiz.objects.all()
    selected_quiz_id = request.GET.get('quiz')
    if selected_quiz_id:
        scores = Score.objects.filter(quiz_id=selected_quiz_id).order_by('-score')[:10]
    else:
        scores = Score.objects.all().order_by('-score')[:10]

    context = {
        'quizzes': quizzes,
        'scores': scores,
    }
    return render(request, 'leaderboard.html', context)
