"""
Admin.py is used to register models on the admin panel,
this will then allow gamekeepers to access these models and
modify them.

This allows game keepers to create new quiz questions
"""

from django.contrib import admin
from .models import Profile, Question

# Models registered by admin and displayed in their profile
admin.site.register(Profile)
admin.site.register(Question)
