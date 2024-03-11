# middleware.py
from datetime import datetime, timedelta
from .models import Bird

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
            if 6 <= now.hour < 12:  # Morning
                if self.last_update_time != None:
                    time_difference = datetime.now() - self.last_update_time
                    bird.health -= int(time_difference.total_seconds() / 3600)
                else:
                    bird.health -= 1
            elif 12 <= now.hour < 18:  # Afternoon
                bird.health -= 1
            else:  # Night
                bird.health -= 1
        
        # Need to add function that decreases mood based on the number of questions answered

            bird.save()
