"""
Load HTML webpages, rendering post requests,
and displaying user specific information

Authors: Maryia Fralova, Ashley Card
"""
from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Score, Quiz
import cv2
import random

# Create your views here.

def home(request):
    template = "home.html"
    context = {}
    return render(request, "home.html", context)#

def navBar(request):
    return render(request, 'navBar.html')
    
def map(request):
    return render(request, "map.html")

# Account views
@login_required
def profile(request):
    return render(request, 'profile.html')

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

@login_required
def logout_view(request):
    logout(request)
    return render(request, 'home.html')

# QR reading views
@login_required
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
        cv2.waitKey(1) # i dont know what this line actually does but it is necessary for the code to work
    cap.release()
    cv2.destroyAllWindows()
    
    #doesn't load page until it gets a qr code; should be accessed from scan page

    #also add more detailed (placeholder) questions page/template

    #data="questions2"
    valid_sites = ["questions1","questions2"]
    context = {"question_page_number":data,"valid":data in valid_sites}
    return render(request, "qr.html",context)



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

def correct_answer(request):
    #this is where the users' score should be updated
    return render(request,"correct_answer.html")

def wrong_answer(request):
    return render(request,"wrong_answer.html")


# Cookie views
def cookiescript(request):
    return render(request, "cookiescript.html")

def cookiepage(request):
    return render(request, "cookiepage.html")
