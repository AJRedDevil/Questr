from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from users.models import *


class Quests(models.Model):
    questrs = models.ForeignKey(QuestrUserProfile)
    pretty_url = models.CharField(_('pretty_url'), 
        max_length=1000)
    description = models.TextField(_('description'))
    title = models.CharField(_('title'), max_length=100, 
        blank=False)
    reward = models.DecimalField(_('reward'), decimal_places=2, 
        max_digits=1000)
    item_images = models.URLField(_('item_images'), blank=True)
    status = models.IntegerField(_('status'), default='0')
    creation_date = models.DateField(_('creation_date'), 
        blank=False)
    # rating = models.IntegerField(_('rating'), default='0')
    # offerers = models.TextField(_('questrs')) # if posted under an offer this would be a single digit (pk of questr object of the offerer)
    # qr_code = models.URLField(_('qr_code'), blank=True)
    srcaddress = models.TextField(_('srcaddress')) # this would be a dict of address attributes 
    location = models.TextField(_('location')) # this would be a city in Toronto
    dstaddress = models.TextField(_('dstaddress')) # this would be a dict of address attributes
    # isprivate = models.BooleanField(_('isprivate'), default=True) # if posted under an offer this would be always set to True, else would be set as False
    isaccepted = models.BooleanField(_('isaccepted'), default=False)

    def __unicode__(self):
        return self.pretty_url 


class QuestComments(models.Model):
    quest = models.ForeignKey(Quests)
    questr = models.ForeignKey(QuestrUserProfile)
    time = models.DateTimeField(_('time'))
    comment = models.TextField(_('comment'))

    def __unicode__(self):
        return self.id