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
    """
    Allows the users to change their passwords if they are logged in.

    Args:
        request (HttpRequest): Will either be a POST or GET request,
                                POST - The password needs to be changed
                                GET  - Load change password form
    Returns:
        render() : When a new user is trying to change the password,
                   change_password.html will load, if they have changed 
                   the password their info will be processed, and redirected
                   to back to change_password.html. If the passwords don't match,
                   the error will be displayed
    """
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
    """
    Allows the users to update their profile information if they are logged in.

    Args:
        request (HttpRequest): Will either be a POST or GET request,
                                POST - The profile information needs to be changed
                                GET  - Load update profile form
    Returns:
        render() : When a new user is trying to edit their profile,
                   profile_update.html will load, if they have changed profile
                   info they will get redirected to profile.html. If the 
                   format of the form is invalid, the error will be displayed
    """
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
    """
    Checks if the purchase of an item from the shop is valid and
    allows users to add it to their inventory if so.

    Args:
        request (HttpRequest)
    Returns:
        JsonResponse(): Item price, type, value are fetched from the POST request.
                  If the user has enough profiles and they have not already 
                  purchased this item, JsonResponse with success[True] is returned.
                  If the user doesn't have enough points, JsonResponse with 
                  success[False, 1]  is returned. If the user has already purchased
                  the item before, JsonResponse with success[False, 0]  is returned. 
    """
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
    """
    First version. Changes the user's avatar

    Args:
        request (HttpRequest)
    Returns:
        HttpResponse(200) : Returns success for the avatar change
    """
    profile = Profile.objects.filter(user=request.user).first()
    new_avatar = request.GET.get('avatar')
    request.user.avatar_choice = new_avatar
    request.user.change_avatar_choice(new_avatar)
    return HttpResponse(200)

@login_required
def profile(request):
    """
    Displays the user's profile page with their Bird avatar

    Args:
        request (HttpRequest)
    Returns:
        render() : Profile page with the user's bird
    """
    bird = Bird.objects.filter(user=request.user).first()
    return render(request, 'profile.html', {'bird': bird})

@login_required
def logout_view(request):
    """
    Logs user out of account and redirects to home page

    Args:
        request (HttpRequest)
    Returns:
        render() : Home page
    """
    logout(request)
    return render(request, 'home.html')

@login_required
def change_avatar(request):
    """
    Second version. Changes the user's avatar when clicked in inventory

    Args:
        request (HttpRequest)
    Returns:
        JsonResponse() : Returns JsonResponse({'success': True}) for successful
                         avatar change, return JsonResponse({'success': False})
                         if there is an error in the avatar change
    """
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
    """
    Puts the accessory onto the bird. Gets the POST values for the type of
    accessory and its value. Updates the bird inventory accordingly.

    Args:
        request (HttpRequest)
    Returns:
        JsonResponse() : Returns JsonResponse({'success': True}) for successful
                         accessory change, return JsonResponse({'success': False})
                         if there is an error in the accessory change
    """
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
    """
    Takes all the bird's accessories off when at POST request is sent.

    Args:
        request (HttpRequest)
    Returns:
        JsonResponse() : Returns JsonResponse({'success': True}) for successful
                         accessory change, return JsonResponse({'success': False})
                         if there is an error in the accessory change
    """
    if request.method == 'POST':
        bird = request.user.bird
        for accessory_type in bird.accessories:
            bird.accessories[accessory_type] = ''
        bird.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def user_page(request, username):
    """
    Displays the user's profile page with their Bird avatar and score
    for another user (the one who is not logged in)

    Args:
        request (HttpRequest)
        username: Username of the user whose profile to display
    Returns:
        render() : user_page.html with the user's bird and score. Passes the user to be displayed
    """
    user = User.objects.get(username=username)
    context = {
        'user': user,
    }
    return render(request, 'user_page.html', context)

def qr(request):
    """
    Analyses the scanned qr code to display the corresponding question type

    Args:
        request (HttpRequest)
    Returns:
        render() : question_format.html that displays a corresponding file with the corresponding
                   question type. If unsuccesssful, HttpResponse with the message that the qr code
                   is invalid.
    """
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

def navBar(request):
    """
    Navigation bar with the links to different pages.

    Args:
        request (HttpRequest)
    Returns:
        render() : Navigation bar page
    """
    return render(request, 'navBar.html')

def home(request):
    """
    Home page of our application, displays the information about the game and
    rules

    Args:
        request (HttpRequest)
    Returns:
        render() : Home page
    """
    template = "home.html"
    context = {}
    return render(request, "home.html", context)

def register(response):
    """
    Displays user registration form for new users, manages POST requests when
    user creates a new account.

    Args:
        request (HttpRequest): Will either be a POST or GET request,
                                POST - User account needs to be created
                                GET  - Load registration form
    Returns:
        render() : When a new user is trying to register an account,
                   register.html will load, if they are creating an
                   account their info will be processed, and redirected
                   to login.html
    """
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
    """
    Page that displays a link to the qr code scanner

    Args:
        request (HttpRequest)
    Returns:
        render() : Scanning page
    """
    return render(request,"scan.html")

def open_file(name):
    """
    Open a file and retrieve a random question of a specified type.

    Args:
        name (str): The type of question to retrieve.

    Returns:
        dict: A dictionary containing the question and answer choices.
            The dictionary has the following keys:
                - 'question': The text of the question.
                - 'answer_1': The text of the first answer choice.
                - 'link_1': The type of the first answer choice ('correct' or 'wrong').
                - 'answer_2': The text of the second answer choice.
                - 'link_2': The type of the second answer choice ('correct' or 'wrong').
                - 'answer_3': The text of the third answer choice.
                - 'link_3': The type of the third answer choice ('correct' or 'wrong').
                - 'answer_4': The text of the fourth answer choice.
                - 'link_4': The type of the fourth answer choice ('correct' or 'wrong').
    """
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

    return context

def correct_answer(request):
    """
    View function to handle correct answers submitted by the user.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: A rendered HTML response for the 'correct_answer' page.

    Behaviour:
        - Retrieves the username of the authenticated user from the request.
        - Updates the user's score, health, and points in the database:
            - Increases the total number of questions answered by 1.
            - Increases the bird's health by 5 if it's less than 95.
            - Increases the user's points by 5.
        - Saves the updated user information in the database.
        - Renders the 'correct_answer.html' template to display the success message.
    """
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
    """
    Page that is displayed when the user's answer was incorrect.

    Args:
        request (HttpRequest)
    Returns:
        render() : Wrong answer page
    """
    return render(request,"wrong_answer.html")

def shop(request):
    """
    View function for displaying the shop page.
    Retrieves the first Shop object from the database and renders the 'shop.html' template
    with the shop data passed as context.

    Args:
        request (HttpRequest): The HTTP request object sent by the client.

    Returns:
        HttpResponse: The HTTP response containing the rendered HTML content of the 'shop.html' template.
            The context includes the 'shop' variable containing the retrieved Shop object.
    """
    shop = Shop.objects.first()
    return render(request, "shop.html", {'shop': shop})

def cookiescript(request):
    """
    Render the 'cookiescript.html' template.
    This view renders the 'cookiescript.html' template, which contains JavaScript code
    related to handling cookies.

    Args:
        request (HttpRequest): The request object generated by Django.

    Returns:
        HttpResponse: A response object that renders the 'cookiescript.html' template.
    """
    return render(request, "cookiescript.html")

def cookiepage(request):
    """
    Render the 'cookiepage.html' template.
    This view renders the 'cookiepage.html' template, which is a page containing information
    about cookies and their usage.

    Args:
        request (HttpRequest): The request object generated by Django.

    Returns:
        HttpResponse: A response object that renders the 'cookiepage.html' template.
    """
    return render(request, "cookiepage.html")

def map(request): 
    """
    Page containing the map, which the user can use to navigate across campus
    to find quiz and minigame locations. Google Maps API is used for that.
    If allow location to be detected, current location will be displayed.

    Args:
        request (HttpRequest)
    Returns:
        render() : map.html, passes in the key to Google Maps API
    """
    Key = settings.GOOGLE_MAPS_API_KEY    
    context ={
        'key':Key
    }

    return render(request, "map.html", context)

def location(request):
    """
    View function for rendering a location-based page.
    This view function retrieves location information using the Google Maps Geocoding API
    and renders a template ('location.html') displaying the retrieved location details.

    Note: This view is currently commented out and not in use. It was intended to force a
    specific location for testing and demonstration purposes. You can uncomment and use this
    view by providing your Google Maps API key ('settings.GOOGLE_MAPS_API_KEY').

    Returns:
        HttpResponse: A response object that renders the 'location.html' template with
        location details.
    """

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
    """
    Render the 'minigame.html' template.
    This view renders the 'minigame.html' template, which contains the interface
    and logic for a mini-game within the web application.

    Args:
        request (HttpRequest): The request object generated by Django.

    Returns:
        HttpResponse: A response object that renders the 'minigame.html' template.
    """
    return render(request,"minigame.html")

def gameover(request):
    """
    Render the 'gameover.html' template.
    This view renders the 'gameover.html' template, which is displayed to the user
    when the game is over or when a specific game condition is met.

    Args:
        request (HttpRequest): The request object generated by Django.

    Returns:
        HttpResponse: A response object that renders the 'gameover.html' template.
    """
    return render(request,"gameover.html")

def get_screen_width(request):
    """
    Retrieve the screen width from a POST request and return it as JSON response.
    This view handles a POST request containing the screen width data. It retrieves
    the screen width value from the request parameters and returns it as a JSON response.

    Args:
        request (HttpRequest): The request object generated by Django.

    Returns:
        JsonResponse: A JSON response containing the screen width if the request is valid,
        otherwise returns a JSON response with an error message.

    Note:
        This view expects a POST request containing the 'screen_width' parameter.
        If the request method is not POST, it returns a JSON response with an error message.
    """
    if request.method == 'POST':
        screen_width = request.POST.get('screen_width')
        return JsonResponse({'screen_width': screen_width})
    else:
        return JsonResponse({'error': 'Invalid request'})

