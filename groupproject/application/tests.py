"""
Tests of application

Author: Maryia Fralova
"""

from django.test import TestCase
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.test.client import Client
from .models import Profile, Bird


# Create your tests here.
class RegisterFormTest(TestCase):
    """
    Tests for the user registration form
    """
    def testValidPassword(self):
        """
        Checks if a user can sign up using a valid password
        """
        form = RegisterForm(data={"username":'testUser', "email":"testEmail@email.com",
                                "password1":"exeternest!454#a", "password2":"exeternest!454#a",
                                "avatar_choice": 'robin'})
        self.assertTrue(form.is_valid())

    def testInvalidPassword(self):
        """
        Checks that the form rejects invalid passwords
        """
        form = RegisterForm(data={"username":'testUser', "email":"testEmail@email.com",
                                "password1":"password", "password2":"password",
                                "avatar_choice": 'robin'})
        self.assertFalse(form.is_valid())

    def testDuplicateUsers(self):
        """
        Checks that two users cant be created with the same username
        """
        user = User.objects.create_user(username='testUser', email="testEmail@email.com", password="exeternest###1234a", is_superuser=1)
        
        form2 = RegisterForm(data={"username":'testUser', "email":"testEmail@email.com",
                                 "password1":"exeternest###1234a", "password2":"exeternest###1234a",
                                 "avatar_choice": 'robin'})
        
        # Assert that the usernames are the same
        self.assertFalse(form2.is_valid())

    def testEmptyUsernameField(self):
        """
        Checks that a username is required
        """
        form = RegisterForm(data={"username":'', "email":"testEmail@email.com",
                                "password1":"exeternest###1234a", "password2":"exeternest###1234a",
                                "avatar_choice": 'robin'})
        self.assertFalse(form.is_valid())

    def testEmptyEmailField(self):
        """
        Checks that a email is required
        """
        form = RegisterForm(data={"username":'testUser', "email":"", "password1":"exeternest###1234a",
                                "password2":"exeternest###1234a", "avatar_choice": 'robin'})
        self.assertFalse(form.is_valid())

    def testEmptyPasswordField(self):
        """
        Checks that a password is required
        """
        form = RegisterForm(data={"username":'testUser', "email":"testEmail@email.com",
                                "password1":"", "password2":"", "avatar_choice": 'robin'})
        self.assertFalse(form.is_valid())


class BirdAccessoriesTest(TestCase):
    """
    Test how the accesseries are put onto the bird
    """
    def testAcessory(self):
        """
        Adds the accessory to the bird and checks if it's added successfully
        """
        # Simulate registration form data
        registration_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'password123!Pass!',
            'password2': 'password123!Pass!',
            'avatar_choice': 'seagull'  # Specify avatar_choice
        }

        # Create a registration form instance with the provided data
        form = RegisterForm(data=registration_data)
        if form.is_valid():
            user = form.save(commit=False)
            user.avatar_choice = form.cleaned_data["avatar_choice"]
            user.save()

        # Check if the form is valid
        self.assertTrue(form.is_valid())

        # Check if the user was created successfully
        self.assertIsNotNone(user)

        # Check if the user has a corresponding profile
        profile = Profile.objects.get(user=user)
        self.assertIsNotNone(profile)

        new_accessory = 'hat10.png'
        new_accessory_type = 'hats'
        user.bird.accessories[new_accessory_type] = new_accessory
        self.assertTrue(user.bird.accessories[new_accessory_type]==new_accessory)


class ResponseTest(TestCase):
    """
    Checks the accessebility of the webpages by checking the HTTP response
    """
    def setUp(self):
        # User form
        form = RegisterForm(data={"username":'testUser', "email":"testEmail@email.com",
                                "password1":"exeternest!454#a", "password2":"exeternest!454#a",
                                "avatar_choice": 'robin'})
        
    def testLoginView(self):
        """
        Test the login view
        """
        response = self.client.get('/login/')
        self.assertEqual(response.status_code,200)

    def testRegistrationView(self):
        """
        Test the register view
        """
        response = self.client.get('/register/')
        self.assertEqual(response.status_code,200)

    def testMapView(self):
        """
        Test the map view
        """
        response = self.client.get('/map/')
        self.assertEqual(response.status_code,200)
    
    def testLeaderboardView(self):
        """
        Test the leaderboard view
        """
        response = self.client.get('/leaderboard/')
        self.assertEqual(response.status_code,200)
    
    def testHomeView(self):
        """
        Test the home view
        """
        response = self.client.get('/home/')
        self.assertEqual(response.status_code,200)


    def testWrongAnswerView(self):
        """
        Test the display for a wrong answer
        """
        response = self.client.get('/application/qr/wrong/')
        self.assertEqual(response.status_code,200) 
    
    def testCookiePageView(self):
        """
        Test the cookie page view
        """
        response = self.client.get('/cookiepage/')
        self.assertEqual(response.status_code,200) 

    def testShopView(self):
        """
        Test the shop view
        """
        response = self.client.get('/shop/')
        self.assertEqual(response.status_code,200) 
    
    def testLocationView(self):
        """
        Test the location view
        """
        response = self.client.get('/location/')
        self.assertEqual(response.status_code,200) 

    def testMinigameView(self):
        """
        Test the minigame view
        """
        response = self.client.get('/minigame/')
        self.assertEqual(response.status_code,200) 
    
    def testMinigameGameoverView(self):
        """
        Test the minigame gameover view
        """
        response = self.client.get('/minigame/gameover/')
        self.assertEqual(response.status_code,200)
        