"""
Defines models for the application

Author: James Gower, Maryia Fralova
"""

from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

class Profile(models.Model):
    """
    Additional information for each user, one to one
    relationship with each User model, auto created
    upon registration

    Args:
        models.Model : Used to define each field
    Attributes:
        user (OneToOneField) : Links Profile to User model
        score (IntegerField) : How many points the user has gained answering quiz questions
        avatar_choice (CharField): What bird the user has selected
    Returns:
        String : Displays name of user on admin site
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Delete profile when user is deleted
    score = models.IntegerField(default=0)
    avatar_choice = models.CharField(max_length=20, default='robin', choices=[('robin', 'Avatar 1'), ('seagull', 'Avatar 2'), ('wren', 'Avatar 3')])

    def __str__(self):
        return f'{self.user.username} Profile' #show how we want it to be displayed

# Will be used to identify the various different quizes
class Quiz(models.Model):
    title = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.title

# Will be used to link a user, the quiz they did, and the score they got
"""class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, default='')
    score = models.IntegerField()

    def __str__(self):
        return f"{self.user.username}'s score on {self.quiz.title}: {self.score}" # will display a users score on a given quiz"""


@receiver(post_save, sender = User)
def user_is_created(sender, instance, created, **kwargs):
    """
    When a user is created, a profile model is also
    setup for the user with a one to one relationship

    Args:
        sender (model): Which model the request has come from
        instance : User which has just registered
        created (Bool): If a user has just been created,
                        and requires a profile model to be setup
    """

    if created:
        Profile.objects.create(user=instance, avatar_choice=instance.avatar_choice)
    else:
        instance.profile.save()

