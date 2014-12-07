

#All Django Imports
from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.files import File
from django.core.files.base import ContentFile
from django.dispatch import receiver
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.utils import six

#All external imports (libs, packages)
import hashlib
import jsonfield
import logging
from rest_framework.authtoken.models import Token

# Init Logger
logger = logging.getLogger(__name__)

VEHICLE_SELECTION = (('car','Sedan'),('minivan','Minivan'))
USERTYPE_SELECTION = (('Courier','Courier'),('Business','Business'))


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

    def create_superuser(self, email, password=None, **extra_fields):
        u = self._create_user(email, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.email_status = True
        u.save(using=self._db)
        return u

    def create_staffuser(self, email, password=None, **extra_fields):
        u = self._create_user(email, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.email_status = True
        u.save(using=self._db)
        return u

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)



class QuestrUserProfile(AbstractBaseUser):
    def upload_pp_path(self, name):
        # name = 'pp'
        folder = self.id
        return str(folder) + '/' + str(name)

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
    avatar = models.ImageField(max_length=1024, upload_to=upload_pp_path, blank=True, default='')
    biography = models.TextField(_('biography'),max_length=9999, blank=True)
    account_status = models.IntegerField(_('account_status'), max_length=1, blank=True, default=1)
    privacy = models.BooleanField(_('privacy'), default=False)
    gender = models.CharField(_('gender'), max_length=1)
    notifications = models.BooleanField(_('notifications'), default=False)
    is_shipper = models.BooleanField(_('is_shipper'), default=False)
    is_staff = models.BooleanField(_('is_staff'), default=False)
    is_superuser = models.BooleanField(_('is_superuser'), default=False)
    rating = models.DecimalField(_('rating'), default='0', max_digits=5, decimal_places=2)
    notificationprefs = jsonfield.JSONField(_('notificationprefs'), default='{}', max_length=9999)
    is_active = models.BooleanField(default=True)
    is_available = models.BooleanField(_('is_available'), default=True)
    address = jsonfield.JSONField(_('address'), default='{}', max_length=9999)
    vehicle = models.CharField(_('vehicle'), max_length=10, default='car', choices=VEHICLE_SELECTION, blank=True)



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','displayname']


    objects = QuestrUserManager()

    def __unicode__(self):
        return self.email 

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def get_short_name(self):
        return self.first_name

    def thumbnail_exists(self, size):
        from django.core.files.storage import default_storage as storage
        return storage.exists(self.avatar.name)

    def __generate_hash(self):
        return hashlib.sha256(str(self.date_joined) + str(self.email)).hexdigest()

    def create_thumbnail(self, size, quality=None):
        # invalidate the cache of the thumbnail with the given size first        
        import os
        from PIL import Image
        from django.core.files.storage import default_storage as storage
        if not self.avatar:
            logger.debug("No item image available")
            return
        file_path = self.avatar.name
        filename_base, filename_ext = os.path.splitext(file_path)
        # try:
        #     os.makedirs(os.path.join(settings.MEDIA_ROOT, str(self.id)+'/ppsize'))
        # except OSError as e:
        #     if e.errno == 17:
        #         # Dir already exists. No biggie.
        #         pass
        avatar_file_path = ('%s'+'_'+self.__generate_hash()[:10]+'.jpg') % (filename_base)
        try:
            if not storage.exists(avatar_file_path):
                try:    
                    orig = storage.open(file_path, 'rb')            
                    image = Image.open(orig)
                    quality = quality or settings.AVATAR_THUMB_QUALITY
                    w, h = image.size
                    if w > h:
                        diff = int((w - h) / 2)
                        image = image.crop((diff, 0, w - diff, h))
                    else:
                        diff = int((h - w) / 2)
                        image = image.crop((0, diff, w, h - diff))
                    if image.mode != "RGB":
                        image = image.convert("RGB")
                    image = image.resize((size, size), Image.ANTIALIAS)
                    # logger.warn(thumb)
                    avatar_image = storage.open(avatar_file_path, "w")
                    image.save(avatar_image, settings.AVATAR_THUMB_FORMAT, quality=quality)
                    avatar_image.close()
                    return avatar_file_path
                except IOError, e:
                    logger.warn(e)
                    return
        except Exception, e:
            return

    def get_profile_pic(self):
        """Returns the url of the aws bucket object"""
        import os
        from django.core.files.storage import default_storage as storage
        default_file_path = settings.STATIC_URL+"img/default.png"
        if not self.avatar:
            return default_file_path
        file_path = self.avatar.name
        logger.warn("file path is %s" % file_path)
        filename_base, filename_ext = os.path.splitext(file_path)
        normal_file_path = ('%s'+'_'+self.__generate_hash()[:10]+'.jpg') % (filename_base)

        ##See if the AWS connection exists or works if doesn't return default file path
        try:
            if storage.exists(normal_file_path):
                # logger.debug(storage.url(normal_file_path))
                return storage.url(normal_file_path)
        except Exception:
            return default_file_path

        return default_file_path

    def save(self, *args, **kwargs):
        super(QuestrUserProfile, self).save(*args, **kwargs)
        if self.avatar:
            # logger.warn("avatar is not None")
            # logger.warn("avatar is %s", self.avatar)
            # if not self.thumbnail_exists(500):
            #     logger.warn("thumbnail doesn't exist")
            self.create_thumbnail(500)
            # super(QuestrUserProfile, self).save(*args, **kwargs)
            

# Create Token for users when a user is created
@receiver(post_save, sender=QuestrUserProfile)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

# User transactionl model
class UserTransactional(models.Model):
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
    timeframe = models.DateTimeField(_('timeframe'), default=timezone.now)

    def is_alive(self):
        timedelta = timezone.now() - self.timeframe
        days = 1
        allowable_time = float(days * 24 * 60 * 60)
        return timedelta.total_seconds() < allowable_time

    def __unicode__(self):
        return "Token verifying ..."

    # Overriding
    def save(self, *args, **kwargs):
        if not self.timeframe:
            self.timeframe = timezone.now()
        super(QuestrToken, self).save(*args, **kwargs)

class UserSignupInvitationToken(models.Model):
    """
    Token Model Class for user's verification, password reset and other such services
    """

    email = models.EmailField(_('email'), max_length=100)
    token = models.CharField(_('id'), max_length=20, primary_key=True)
    timeframe = models.DateTimeField(_('timeframe'), default=timezone.now)
    status = models.BooleanField(_('status'), default=False)
    invitation_type = models.CharField(_('invitation_type'), max_length=20, default="Courier")

    def is_alive(self):
        timedelta = timezone.now() - self.timeframe
        days = 1
        allowable_time = float(days * 24 * 60 * 60)
        return timedelta.total_seconds() < allowable_time

    def get_token(self):
        return self.token

    def generate_token(self):
        """
        Generates a token with first 14 hash and last 6 as verification code
        """
        import uuid
        strhash = hashlib.sha256(str(timezone.now()) + str(uuid.uuid4())).hexdigest()[:20]
        return strhash

    def __unicode__(self):
        return self.token

    # Overriding
    def save(self, *args, **kwargs):
        # Tag all existing tokens from this user as used before creating new
        UserSignupInvitationToken.objects.filter(email=self.email).update(status=True)
        self.token = self.generate_token()
        super(UserSignupInvitationToken, self).save(*args, **kwargs)

class UserEvents(models.Model):
    """Models for Users UserEvents"""
    current_time = timezone.now

    questr = models.ForeignKey(QuestrUserProfile)
    event = models.IntegerField(_('event'), max_length=2, default=1)
    updated_on = models.DateTimeField(_('updated_on'), 
        default=current_time)
    extrainfo = jsonfield.JSONField(_('extrainfo'), default='{}', max_length=9999)

    
    def save(self, *args, **kwargs):
        if not self.updated_on:
            self.updated_on = timezone.now
        super(UserEvents, self).save(*args, **kwargs)
