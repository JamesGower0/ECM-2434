from django.test import TestCase
from .forms import SignUpForm


# Create your tests here.
class RegisterFormTest(TestCase):
    """
    Tests for the user registration form
    """
    def testValidPassword(self):
        """
        Checks if a user can sign up using a valid password
        """
        form = SignUpForm(data={"username":'testUser', "email":"testEmail@email.com",
                                "password1":"exeternest###1234a", "password2":"exeternest###1234a",
                                "avatar_choice": ('robin', 'Avatar 1')})
        self.assertTrue(form.is_valid())

    def testInvalidPassword(self):
        """
        Checks that the form rejects invalid passwords
        """
        form = SignUpForm(data={"username":'testUser', "email":"testEmail@email.com",
                                "password1":"password", "password2":"password",
                                "avatar_choice": ('robin', 'Avatar 1')})
        self.assertFalse(form.is_valid())

    def testDuplicateUsers(self):
        """
        Checks that two users cant be created with the same username
        """
        form = SignUpForm(data={"username":'testUser', "email":"testEmail@email.com",
                                "password1":"exeternest###1234a", "password2":"exeternest###1234a",
                                "avatar_choice": ('robin', 'Avatar 1')})
        form.save()
        form2 = SignUpForm(data={"username":'testUser', "email":"testEmail@email.com",
                                 "password1":"exeternest###1234a", "password2":"exeternest###1234a",
                                 "avatar_choice": ('robin', 'Avatar 1')})
        self.assertFalse(form2.is_valid())

    def testEmptyUsernameField(self):
        """
        Checks that a username is required
        """
        form = SignUpForm(data={"username":'', "email":"testEmail@email.com",
                                "password1":"exeternest###1234a", "password2":"exeternest###1234a",
                                "avatar_choice": ('robin', 'Avatar 1')})
        self.assertFalse(form.is_valid())

    def testEmptyEmailField(self):
        """
        Checks that a email is required
        """
        form = SignUpForm(data={"username":'testUser', "email":"", "password1":"exeternest###1234a",
                                "password2":"exeternest###1234a", "avatar_choice": ('robin', 'Avatar 1')})
        self.assertFalse(form.is_valid())

    def testEmptyPasswordField(self):
        """
        Checks that a password is required
        """
        form = SignUpForm(data={"username":'testUser', "email":"testEmail@email.com",
                                "password1":"", "password2":"", "avatar_choice": ('robin', 'Avatar 1')})
        self.assertFalse(form.is_valid())