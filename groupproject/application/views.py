"""
Load HTML webpages, rendering post requests,
and displaying user specific information

Authors: Maryia Fralova, Ashley Card, James Gower, Aidan Daniel, Tom Evans

"""
from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
#from .models import Score, Quiz
from .models import Quiz, Profile, User
import cv2
import random
import csv
import googlemaps
from django.conf import settings

# Create your views here.

@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def logout_view(request):
    logout(request)
    return render(request, 'home.html')

def qr(request):
    
    #reads the qr code

    
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()
    while True:
        _, img = cap.read()
        data, bbox, _ = detector.detectAndDecode(img)
        if bbox is not None:
            if data:
                break   
        cv2.waitKey(1) 
    cap.release()
    cv2.destroyAllWindows()
    
    #doesn't load page until it gets a qr code; should be accessed from scan page

    valid_sites = ["questions1","questions2","questions3","questions4","questions5"]
    context = {"question_page_number":data,"valid":data in valid_sites}
    return render(request, "qr.html",context)

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
            user.avatar_choice = form.cleaned_data["avatar_choice"]
            user.save()
            return redirect("/login/")
    else:
        form = forms.RegisterForm()

    return render(response, "register.html", {"form":form})

def leaderboard(request):
    # THE FOLLOWING CODE WILL BE USED FOR THE SECOND SPRINT, DONT DELETE
    """quizzes = Quiz.objects.all()
    selected_quiz_id = request.GET.get('quiz')
    if selected_quiz_id:
        scores = Score.objects.filter(quiz_id=selected_quiz_id).order_by('-score')[:10]
    else:
        scores = Score.objects.all().order_by('-score')[:10]

    context = {
        'quizzes': quizzes,
        'scores': scores,
    }
    return render(request, 'leaderboard.html', context)"""

    users = User.objects.all()
    headers = ["Place", "Bird name", "Username", "Score"]
    profiles = Profile.objects.order_by('-score')[0:10]
    
    return render(request, 'leaderboard.html', {'users': users, 'headers': headers, 'profiles': profiles})

def scan(request):
    #This should be the first page of the qr functionality; the one linked to from elsewhere
    #has a link to the qr page and ask to scan a qr code
    return render(request,"scan.html")

def open_file(name):
    file = open('application/'+name,'r')
    file = file.readlines()
    #pick a random question from the file
    r = random.randint(0,(len(file)-1))
    question = file[r]
    question = question.split(',')
    context = {"question":question[0],"correct_answer":question[1],"wrong_1":question[2],"wrong_2":question[3],"wrong_3":question[4],}
    return context

def questions1(request):
    #each of these views should correspond to a different file of questions
    #in the format of example_questions.csv
    file_name = 'Biodiversity questions.csv'
    context = open_file(file_name)
    return render(request,"question_format.html",context)

def questions2(request):
    file_name = 'Construction questions.csv'
    context = open_file(file_name)
    return render(request,"question_format.html",context)

def questions3(request):
    file_name = 'Exercise questions.csv'
    context = open_file(file_name)
    return render(request,"question_format.html",context)

def questions4(request):
    file_name = 'Personal impact questions.csv'
    context = open_file(file_name)
    return render(request,"question_format.html",context)

def questions5(request):
    file_name = 'Research questions.csv'
    context = open_file(file_name)
    return render(request,"question_format.html",context)

# Writes the players scores to scores.csv
def correct_answer(request):
    username = request.user.get_username()

    # Updating user's score and saving into the database
    current_user = request.user
    current_user.profile.score += 1
    current_user.save()
    return render(request,"correct_answer.html")

# Getting a question wrong doesnt affect the users score so doesnt edit scores.csv
def wrong_answer(request):
    return render(request,"wrong_answer.html")

def cookiescript(request):
    return render(request, "cookiescript.html")

def cookiepage(request):
    return render(request, "cookiepage.html")

def map(request): 
    Key = settings.GOOGLE_MAPS_API_KEY
    gmaps = googlemaps.Client(key = Key)
    result = gmaps.geocode('Stocker Rd, Exeter EX4 4PY')[0]

    # when testing you can hard code latitude and longditude values by commenting the follwoing two lines and manually
    # defining lat and lng (to show what it would do at specific coords)
    lat = result.get("geometry", {}).get("location", {}).get("lat", None)
    lng = result.get("geometry", {}).get("location", {}).get("lng", None)

    context ={
        'result':result,
        'lat':lat,
        'lng':lng,
        'key':Key
    }

    return render(request, "map.html", context)