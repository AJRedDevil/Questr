from django import forms
from django.db import models
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    email_status = models.BooleanField(default=False)
    password_status = models.BooleanField(default=False)
    phone = models.IntegerField(max_length=15, blank=True)
    avatar_file_name = models.CharField(max_length=765, blank=True)
    social_networks = models.TextField(blank=False)
    account_status = models.IntegerField(max_length=1, blank=False)