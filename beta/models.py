from django import forms
from django.db import models

class Contact(models.Model):
	email = models.EmailField()
