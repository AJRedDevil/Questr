from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class QuestrUserProfile(AbstractUser):
    email_status = models.BooleanField(default=False, blank=False)
    phone = models.CharField(max_length=15, blank=True)
    avatar_file_name = models.CharField(_('avatar_file_name'),max_length=765, blank=True)
    biography = models.TextField(_('biography'),max_length=9999, blank=True)
    account_status = models.IntegerField(_('account_status'), max_length=1, blank=True, default=1)
    privacytoggle = models.BooleanField(default=False, blank=False)
    gender = models.CharField(max_length=1, blank=False)