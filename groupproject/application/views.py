"""
Load HTML webpages, rendering post requests,
and displaying user specific information

Authors: Maryia Fralova, Ashley Card, James Gower, Aidan Daniel, Tom Evans

"""
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponse, JsonResponse
from . import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, update_session_auth_hash
#from .models import Score, Quiz
from .models import Quiz, Profile, User, Bird, Shop, Question
import cv2
import random
import csv
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
import googlemaps
from django.conf import settings

# Create your views here.
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Successfully updated')
            return redirect('change_password')
        else:
            messages.error(request, 'error')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
        })
@login_required
def profile_update(request):
    if request.method=='POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,

    }
    return render(request, 'profile_update.html', context)

@login_required
def buy_item(request):
    if request.method == 'POST':
        profile = Profile.objects.filter(user=request.user).first()
        item_price = int(request.POST.get('item_price'))
        item_type = request.POST.get('item_type')
        item_value = request.POST.get('item_value')[:-4]
        # Checking if the user has enough points to buy an item
        if profile.points >= item_price:
            # Checking if the user has already bought this item
            if item_value in profile.inventory[item_type]:
                return JsonResponse({'success': [False, 0]})
            profile.remove_points(item_price)
            profile.add_item_to_json_field(item_type, item_value)
            profile.save()
            # or return http respone if ajax
            return JsonResponse({'success': [True]})
        else:
            return JsonResponse({'success': [False, 1]})

@login_required
def changepic(request):
    profile = Profile.objects.filter(user=request.user).first()
    new_avatar = request.GET.get('avatar')
    print(new_avatar)
    request.user.avatar_choice = new_avatar
    print(request.user.avatar_choice)
    request.user.change_avatar_choice(new_avatar)
    return HttpResponse(200)

@login_required
def profile(request):
    bird = Bird.objects.filter(user=request.user).first()
    return render(request, 'profile.html', {'bird': bird})

@login_required
def logout_view(request):
    logout(request)
    return render(request, 'home.html')

@login_required
def change_avatar(request):
    if request.method == 'POST':
        new_avatar = request.POST.get('new_avatar')
        if new_avatar:
            # Assuming you have authenticated user
            profile = request.user.profile
            profile.avatar_choice = new_avatar
            profile.save()
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@login_required
def add_accessory(request):
    if request.method == 'POST':
        # Need to change the accessories on the Bird
        new_accessory = request.POST.get('new_accessory')
        new_accessory_type = request.POST.get('new_accessory_type')
        if new_accessory and new_accessory_type:
            # Assuming you have authenticated user
            bird = request.user.bird
            if bird.accessories[new_accessory_type] == new_accessory:
                bird.accessories[new_accessory_type] = ''
            else:
                bird.accessories[new_accessory_type] = new_accessory
            bird.save()
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def empty_accessories(request):
    if request.method == 'POST':
        bird = request.user.bird
        for accessory_type in bird.accessories:
            bird.accessories[accessory_type] = ''
        bird.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def user_page(request, username):
    user = User.objects.get(username=username)
    context = {
        'user': user,
        # Other context data if any
    }
    return render(request, 'user_page.html', context)

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

    #the above code is for the qr functionality; the data variable is what should be used to access different questions
    QNum = request.GET.get('QNum')
    data = "questions" + QNum

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
    # Change the total number of questions answered
    current_user.profile.score += 1
    # Increase health by 1 if not 100
    if current_user.bird.health < 95:
        current_user.bird.health += 5
    # Increase points by 5
    current_user.profile.points += 5
    
    current_user.save()
    return render(request,"correct_answer.html")

# Getting a question wrong doesnt affect the users score so doesnt edit scores.csv
def wrong_answer(request):
    return render(request,"wrong_answer.html")

def shop(request):
    shop = Shop.objects.first()
    return render(request, "shop.html", {'shop': shop})

def cookiescript(request):
    return render(request, "cookiescript.html")

def cookiepage(request):
    return render(request, "cookiepage.html")

def map(request): 
    Key = settings.GOOGLE_MAPS_API_KEY    
    context ={
        'key':Key
    }

    return render(request, "map.html", context)

def location(request):
    '''
    Will be used to force a location when testing and demonstrating

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
    }'''

    return render(request, "location.html")

def minigame(request):
    return render(request,"minigame.html")

def gameover(request):
    return render(request,"gameover.html")

def get_screen_width(request):
    if request.method == 'POST':
        screen_width = request.POST.get('screen_width')
        return JsonResponse({'screen_width': screen_width})
    else:
        return JsonResponse({'error': 'Invalid request'})

