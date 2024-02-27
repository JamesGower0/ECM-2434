"""
Tests of application

Author: Maryia Fralova
"""

from django.test import TestCase
from .forms import RegisterForm
from django.contrib.auth.models import User


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
        user = User.objects.create_user(username='testUser', email='testEmail@email.com', password='exeternest###1234a')
        
        form2 = RegisterForm(data={"username":'testUser', "email":"testEmail@email.com",
                                 "password1":"exeternest###1234a", "password2":"exeternest###1234a",
                                 "avatar_choice": 'robin'})
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
        