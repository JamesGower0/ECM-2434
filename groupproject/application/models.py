"""
Defines models for the application

Author:
"""

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Delete profile when user is deleted
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile' #show how we want it to be displayed

class Quiz(models.Model):
    title = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.title

class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, default='')
    score = models.IntegerField()

    def __str__(self):
        return f"{self.user.username}'s score on {self.quiz.title}: {self.score}"
    

