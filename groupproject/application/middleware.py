"""
Dynamically updates the bird health every hours from 8am until 4pm

Author: Maryia Fralova
"""

from datetime import datetime, timedelta
from .models import Bird, Profile, User

class BirdMetricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.last_update_time = None

    def __call__(self, request):
        # Check if an hour has passed since the last update
        if not self.last_update_time or datetime.now() - self.last_update_time >= timedelta(hours=1):
            # Update bird metrics based on time of day or any other conditions
            self.update_bird_metrics()
            # Update the last update time
            self.last_update_time = datetime.now()

        response = self.get_response(request)
        return response

    def update_bird_metrics(self):
        birds = Bird.objects.all()

        now = datetime.now()
        for bird in birds:
            if bird.health > 0:
                if 8 <= now.hour < 16:  # From 8am until 4pm the health is changed
                    if self.last_update_time != None:
                        time_difference = datetime.now() - self.last_update_time
                        bird.health -= int(time_difference.total_seconds() / 3600)
                    else:
                        bird.health -= 1
            if bird.health == 0:
                user = User.objects.get(id=bird.user_id)
                profile = Profile.objects.get(user_id = user.id)
                if 8 <= now.hour < 20:
                    if profile.points > 0:
                        if self.last_update_time != None:
                            time_difference = datetime.now() - self.last_update_time
                            profile.points -= int(time_difference.total_seconds() / 3600)

                            profile.save()
            bird.save()