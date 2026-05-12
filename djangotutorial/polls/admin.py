"""
Admin interface configuration for the polls app.
"""

from django.contrib import admin
from .models import Question

admin.site.register(Question)
