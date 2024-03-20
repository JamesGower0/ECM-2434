"""
Defines models for the application

Author: James Gower, Maryia Fralova
"""

from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


def default_json():
    return {
        'hats': [],
        'bows': [],
        'item_left': [],
        'birds': [],
    }

def default_json_shop():
    return {
        'hats':  [['hat1.png', 5],['hat2.png', 10]],
        'bows':  [['bow1.png', 5], ['bow2.png', 10]],
        'shoes': [['shoes1.png', 5], ['shoes2.png', 10]],
        'birds': [['robin.png', 10], ['seagull.png', 10], ['wren.png', 10]],
    }


def default_json_bird():
    return {
        'hats': '',
        'bows': '',
        'item_left': '',
    }


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
    # Total number of questions answered
    score = models.IntegerField(default=0)
    # Points
    points = models.IntegerField(default=0)
    avatar_choice = models.CharField(max_length=20, default='robin', choices=[('robin', 'Avatar 1'), ('seagull', 'Avatar 2'), ('wren', 'Avatar 3')])

    # Stores all the items purchased by the user
    inventory = models.JSONField(default=default_json)

    def change_avatar_choice(self, value):
        self.avatar_choice = value
        self.save()

    def remove_points(self, value):
        self.points -= value
        self.save()
        
    def add_item_to_json_field(self, key, value):
        """
        Function to add items to the JSONField later.
        """
        json_data = self.inventory or {}

        # Ensure the key exists in the JSON data
        if key not in json_data:
            json_data[key] = []
        else:
            json_data[key].append(value)

        # If the key is 'birds', set the avatar_choice value
        #if key == 'birds':
        #    json_data['birds'].append(value)

        self.inventory = json_data

        self.save()

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


class Bird(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Delete profile when user is deleted
    # Should be created when the user is registered (add to user_is_created function below) 
    birdType = models.CharField(max_length=20, default='robin')
    # Depends on the correctness of the answers; Can be increased by correct answers
    health = models.IntegerField(default=100)
    # Accessories ON the bird
    accessories = models.JSONField(default=default_json_bird) 

    def __str__(self):
        return f'{self.birdType} Bird'
    

class SingletonShopManager(models.Manager):
    def get_or_create_singleton(self):
        obj, created = self.get_or_create(pk=1)
        return obj

class Shop(models.Model):
    accessories = models.JSONField(default=default_json_shop)

    objects = SingletonShopManager()

    def __str__(self):
        return f'Shop'

    class Meta:
        verbose_name = 'Shop'
        verbose_name_plural = 'Shop'


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
        if instance.is_superuser == 1:
            Bird.objects.create(user=instance, birdType = 'robin')
            profile_instance = Profile.objects.create(user=instance)
            profile_instance.add_item_to_json_field('birds', 'robin')
        else:
            profile_instance = Profile.objects.create(user=instance, avatar_choice=instance.avatar_choice)
            Bird.objects.create(user=instance, birdType = instance.avatar_choice)
            profile_instance.add_item_to_json_field('birds', instance.avatar_choice)
    else:
        instance.profile.save()
        instance.bird.save()

class Question(models.Model):
    type = models.CharField(max_length=256)
    text = models.CharField(max_length=256)
    correct = models.CharField(max_length=256)
    wrong_1 = models.CharField(max_length=256)
    wrong_2 = models.CharField(max_length=256)
    wrong_3 = models.CharField(max_length=256)
    def get_type(self):
        return self.type
    def return_values(self):
        values = (self.text,self.correct,self.wrong_1,self.wrong_2,self.wrong_3)
        return(values)