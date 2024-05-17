from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def get_by_natural_key(self, email):
        return self.get(email=email)

class User(AbstractBaseUser):
    USER_ROLES = (
        ('mentor', 'Mentor'),
        ('mentee', 'Mentee'),
        ('admin', 'Admin'),
    )
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    address = models.CharField(max_length=255)
    bio = models.TextField(blank=True, null=True)
    occupation = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=10, choices=USER_ROLES, default='mentee', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    expertise = models.CharField(max_length=255, blank=True, null=True)
    occupation = models.CharField(max_length=255, blank=True, null=True)

    USERNAME_FIELD = 'email'
    
    objects = UserManager()  
    
    def __str__(self):
        return self.email
    

class MentorshipSession(models.Model):
    mentor = models.ForeignKey(User, on_delete=models.CASCADE)
    mentee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentee_sessions')
    date = models.DateField()
    time = models.TimeField()
    STATUS = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined')
    )
    status = models.CharField(max_length=20, choices=STATUS, default='pending')

class Review(models.Model):
    mentorshipSession = models.ForeignKey(MentorshipSession, on_delete=models.CASCADE, default=None, related_name='reviews')
    rating = models.IntegerField()
    review_text = models.TextField()
