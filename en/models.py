from django.db import models
from django.forms import CharField, Form, PasswordInput
from django.core.validators import MinValueValidator, MaxValueValidator

class User(models.Model):
    reg_date = models.DateTimeField('date published')
    name = models.CharField(max_length=25)
    email = models.EmailField(max_length=254, unique=True)
    profile_pic = models.ImageField()
    password = model.CharField(widget=PasswordInput())
    ratings = models.DecimalField(max_digits=4, decimal_places=1)

class Quest(models.Model):
    user = models.ForeignKey(User) # A quest belongs to only one user as OP 
    pub_date = models.DateTimeField('date published')
    is_independent = models.BooleanField(default=True)
    bounty = models.PositiveIntegerField()
    description = models.TextField()

class Offer(models.Model):
    user = models.ForeignKey(User) # An offer belongs to only one user as OP
    pub_date = models.DateTimeField('date published')
    is_independent = models.BooleanField(default=True)
    countdown = models.PositiveIntegerField()
    description = models.TextField()
    
class Review(models.Model):
    user = models.ForeignKey(User, related_name='review_of')
    from_user = models.OneToOneField(User, related_name='review_from')
    pub_date = models.DateTimeField('date published')
    rating = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(5)])
    
class Location(models.Model):
