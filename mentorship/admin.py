from django.contrib import admin

# Register your models here.
from .models import User, MentorshipSession, Review

admin.site.register(User)
admin.site.register(MentorshipSession)
admin.site.register(Review)