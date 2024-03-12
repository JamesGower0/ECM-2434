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
from .models import Quiz, Profile, User, Question
import cv2
import random
import csv

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

    
    #cap = cv2.VideoCapture(0)
    #detector = cv2.QRCodeDetector()
    #while True:
     #   _, img = cap.read()
      #  data, bbox, _ = detector.detectAndDecode(img)
       # if bbox is not None:
        #    if data:
         #       break   
        #cv2.waitKey(1) 
    #cap.release()
    #cv2.destroyAllWindows()
    
    #doesn't load page until it gets a qr code; should be accessed from scan page

    valid_sites = ["questions1","questions2","questions3","questions4","questions5"]


    #the above code is for the qr functionality; the data variable is what should be used to access different questions
    data = "questions2"

    #   !COMBINE WITH QUESTION VIEW!
    file_name=None
    if data == "questions1":
        file_name = 'Biodiversity questions.csv'
    elif data == "questions2":
        file_name = 'Construction questions.csv'
    elif data == "questions3":
        file_name = 'Exercise questions.csv'
    elif data == "questions4":
        file_name = 'Personal impact questions.csv'
    elif data == "questions5":
        file_name = 'Research questions.csv'
    else:
        return HttpResponse("not a valid qr code")
    context = open_file(file_name)
    return render(request,"question_format.html",context)


    #note that the 'qr', 'questions1' and 'questions2' templates are also obsolete and should be deleted

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

    # !! will be replaced by database model 
    #file = open('application/'+name,'r')
    #file = file.readlines()
    #pick a random question from the file
    #r = random.randint(0,(len(file)-1))
    #question = file[r]
    #question = question.split(',')
    #!!

    all_question_objects = Question.objects.all()
    all_questions = []

    for i in range(0,len(all_question_objects)):
        c_question_object = all_question_objects[i]
        c_question = c_question_object.return_values()
        if c_question_object.get_type() == name:
            all_questions.append(c_question)

    r = random.randint(0,len(all_questions)-1)
    question = all_questions[r]

    new_list = []
    new_list.append(question[0])
    new_list.append((question[1],"correct"))
    new_list.append((question[2],"wrong"))
    new_list.append((question[3],"wrong"))
    new_list.append((question[4],"wrong"))

    r2 = random.randint(1,4)
    temp_c = new_list[r2]
    new_list[r2] = new_list[1]
    new_list[1] = temp_c

    context = {"question":new_list[0],
               "answer_1":new_list[1][0],
               "link_1":new_list[1][1],
               "answer_2":new_list[2][0],
               "link_2":new_list[2][1],
               "answer_3":new_list[3][0],
               "link_3":new_list[3][1],
               "answer_4":new_list[4][0],
               "link_4":new_list[4][1],}

    #context = {"question":question[0],"correct_answer":question[1],"wrong_1":question[2],"wrong_2":question[3],"wrong_3":question[4],}
    return context

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

def map(request):
    return render(request, "map.html")

def cookiescript(request):
    return render(request, "cookiescript.html")

def cookiepage(request):
    return render(request, "cookiepage.html")
