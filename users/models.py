

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

import jsonfield
import hashlib

# Create your models here.
class QuestrUserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()

        if not email:
            raise ValueError('The given email must be set')
            
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_active=True, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)



class QuestrUserProfile(AbstractBaseUser):
    id = models.AutoField(_('id'), primary_key=True)
    displayname = models.CharField(_('displayname'), max_length=30, unique=True, 
        error_messages={'unique' : 'The username provided is already taken !'})
    first_name = models.CharField(_('first_name'), max_length=30)
    last_name = models.CharField(_('last_name'), max_length=30)
    email = models.EmailField(_('email'), max_length=100, unique=True,
        error_messages={'unique' : 'It seems you already have an account registered with that email!'})

    email_status = models.BooleanField(_('email_status'), default=False)
    phone = models.CharField(_('phone'), max_length=15, blank=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    avatar_file_name = models.ImageField(max_length=9999, upload_to='ppsize')
    biography = models.TextField(_('biography'),max_length=9999, blank=True)
    account_status = models.IntegerField(_('account_status'), max_length=1, blank=True, default=1)
    privacy = models.BooleanField(_('privacy'), default=False)
    gender = models.CharField(_('gender'), max_length=1)
    notifications = models.BooleanField(_('notifications'), default=False)
    is_shipper = models.BooleanField(_('is_shipper'), default=False)
    rating = models.DecimalField(_('rating'), default='0', max_digits=5, decimal_places=2)
    notificationprefs = jsonfield.JSONField(_('notificationprefs'), default='{}', max_length=9999)
    is_active = models.BooleanField(default=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','displayname']


    objects = QuestrUserManager()

    def __unicode__(self):
        return self.email 

    def get_full_name(self):
        return self.first_name + " " + self.last_name

# User transactionl model
class UserTransactional(models.Model):
    id = models.IntegerField(_('id'), primary_key=True)
    user_code = models.CharField(_('user_code'), max_length=64, unique=True)
    email = models.EmailField(_('email'), max_length=100)
    status = models.BooleanField(_('status'), default=False)

    def generate_hash(self):
        return hashlib.sha256(str(timezone.now()) + str(self.email)).hexdigest()

    def get_truncated_user_code(self):
        return self.user_code[:7]

    def get_token_id(self):
        return self.user_code[-6:]

    REQUIRED_FIELDS = ['user_code', 'id']

    def __unicode__(self):
        return "{0}:{1} {2}".format(self.user_code, self.id, self.email)

    #Overriding
    def save(self, *args, **kwargs):
        #check if the row with this hash already exists.
        if not self.user_code:
            self.user_code = self.generate_hash()
        # self.my_stuff = 'something I want to save in that field'
        super(UserTransactional, self).save(*args, **kwargs)

# Questr Token
class QuestrToken(models.Model):
    token_id = models.CharField(_('id'), max_length=20, primary_key=True)
    timeframe = models.DateTimeField(_('create_date'), default=timezone.now)

    def is_alive(self):
        timedelta = timezone.now() - self.timeframe
        days = 4
        allowable_time = float(days * 24 * 60 * 60)
        return timedelta.total_seconds() < allowable_time

    def __unicode__(self):
        return "Token verifying ..."

    # Overriding
    def save(self, *args, **kwargs):
        if not self.timeframe:
            self.timeframe = timezone.now()
        super(QuestrToken, self).save(*args, **kwargs)