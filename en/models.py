from django.db import models
#from django.forms import CharField, Form, PasswordInput
from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

class Location(models.Model):
    location = models.CharField(max_length=64)
    def __unicode__(self):  # Python 3: def __str__(self):
        string = "id: \t" + str(self.id) + ",\n\tname: \t" + self.location
        return string

class User(models.Model):
    reg_date = models.DateTimeField('date published')
    name = models.CharField(max_length=25)
    email = models.EmailField(max_length=254, unique=True)
    profile_pic = models.ImageField(upload_to='profile_pic/', height_field=900, width_field=900)
    password = models.CharField(max_length=32)
    ratings = models.DecimalField(max_digits=4, decimal_places=1, default=0.0)
    recommended = models.BooleanField(default=False) # Best users

    def __unicode__(self):  # Python 3: def __str__(self):
        string = "id: \t" + str(self.id) + ",\n\tname: \t" + self.name + ".\n"
        return string

############### Quest and its denpendent ###########################
"""
Class Quest is an independent post, as opposed to the later QuesetBid
"""
class Quest(models.Model):
    user = models.ForeignKey(User) # A quest belongs to only one user as OP 
    pub_date = models.DateTimeField('date published')
    countdown = models.PositiveIntegerField(default=7) # expiry date for looking for offers
    location1 = models.ForeignKey(Location, related_name='im_in') # I'm in ________
    location2 = models.ForeignKey(Location, related_name='need_stuff_from') # and I need stuff from ________
    postal_code = models.CharField(max_length=32)
    bounty = models.PositiveIntegerField()  # and I'm offering $_______
    description = models.TextField()
    attachement = models.ImageField(upload_to='images/quest/', height_field=4000, width_field=4000)
    recommended = models.BooleanField(default=False) # Best Quests for homepage
    bid_count = models.PositiveIntegerField(default=0)

    def __unicode__(self):  # Python 3: def __str__(self):
        string = "id: \t" + str(self.id) + ",\n\tI'm in " + self.location1.location + " and I need stuff from " + self.location2.location + " and I'm offering $" + str(self.bounty) + ".\n"
        return string

"""
Class OfferBid is a dependent post on a Quest, as opposed to the later Offer
"""
class OfferBid(models.Model):
    user = models.ForeignKey(User) # An offerbid belongs to only one user as OP
    affiliated_to = models.ForeignKey(Quest) # Multiple offers under one quest
    pub_date = models.DateTimeField('date published')
    location1 = models.ForeignKey(Location, related_name='im_going_to_bid')   # I'm going to ________
    location2 = models.ForeignKey(Location, related_name='from_bid')   # from ________
    postal_code = models.CharField(max_length=32)
    countdown = models.PositiveIntegerField() # in ___ days
    description = models.TextField()
    attachement = models.ImageField(upload_to='images/offer_bid/', height_field=4000, width_field=4000)
    recommended = models.BooleanField(default=False) # Best Offers for homepage

    def __unicode__(self):  # Python 3: def __str__(self):
        string = "id: \t" + str(self.id) + ",\n\tI'm going to " + self.location1.location + "from " + self.location2.location + " in " + str(self.countdown) + " days.\n"
        return string

############### Offer and its denpendent ###########################

"""
Class Offer is an independent post, as opposed to the earlier OfferBid
"""
class Offer(models.Model):
    user = models.ForeignKey(User) # An offer belongs to only one user as OP
    pub_date = models.DateTimeField('date published')
    location1 = models.ForeignKey(Location, related_name='im_going_to')   # I'm going to ________
    location2 = models.ForeignKey(Location, related_name='from')   # from ________
    postal_code = models.CharField(max_length=32)
    countdown = models.PositiveIntegerField() # in ___ days
    
    description = models.TextField()
    attachement = models.ImageField(upload_to='images/offer/', height_field=4000, width_field=4000)
    recommended = models.BooleanField(default=False) # Best Offers for homepage
    bid_count = models.PositiveIntegerField(default=0)

    def __unicode__(self):  # Python 3: def __str__(self):
        string = "id: \t" + str(self.id) + ",\n\tI'm going to " + self.location1.location + " from " + self.location2.location + " in " + str(self.countdown) + " days.\n"
        return string

"""
Class QuestBid is a dependent post on an Offer, as opposed to the earlier Quest
"""
class QuestBid(models.Model):
    user    = models.ForeignKey(User) # A questbid belongs to only one user as OP
    affiliated_to = models.ForeignKey(Offer) # Multiple offers under one offer
    pub_date = models.DateTimeField('date published')
    countdown = models.PositiveIntegerField(default=7) # expiry date for looking for offers
    location1 = models.ForeignKey(Location, related_name='im_in_bid') # I'm in ________
    location2 = models.ForeignKey(Location, related_name='need_stuff_from_bid') # and I need stuff from ________
    postal_code = models.CharField(max_length=32)
    bounty = models.PositiveIntegerField()  # and I'm offering $_______
    description = models.TextField()
    attachement = models.ImageField(upload_to='images/questbid/', height_field=4000, width_field=4000)
    recommended = models.BooleanField(default=False) # Best Quests for homepage
    
    def __unicode__(self):  # Python 3: def __str__(self):
        string = "id: \t" + str(self.id) + ",\n\tI'm in " + self.location1.location + " and I need stuff from " + self.location2.location + " and I'm offering $" + str(self.bounty) + ".\n"
        return string


    
class Review(models.Model):
    user = models.ForeignKey(User, related_name='review_of')
    from_user = models.OneToOneField(User, related_name='review_from')
    pub_date = models.DateTimeField('date published')
    rating = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(5)])
    
