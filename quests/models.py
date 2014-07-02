from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from users.models import *

import logging

class Quests(models.Model):
    questrs = models.ForeignKey(QuestrUserProfile)
    # pretty_url = models.CharField(_('pretty_url'), 
    #     max_length=1000, blank=True)
    description = models.TextField(_('description'))
    title = models.CharField(_('title'), max_length=100, 
        blank=False)
    reward = models.DecimalField(_('reward'), decimal_places=2, 
        max_digits=1000)
    item_images = models.URLField(_('item_images'), blank=True)
    status = models.TextField(_('status'), default='new')
    creation_date = models.DateTimeField(_('creation_date'), 
        blank=False)
    size = models.TextField(_('size'), default="backpack")
    # rating = models.IntegerField(_('rating'), default='0')
    shipper = models.TextField(_('shipper'), blank=True, null=True) # if posted under an offer this would be a single digit (pk of questr object of the offerer)
    # qr_code = models.URLField(_('qr_code'), blank=True)
    srccity = models.TextField(_('srccity'), default="Toronto") # this is the source city
    dstcity = models.TextField(_('dstcity'), default="Toronto") # this is the destination city
    srcaddress = models.TextField(_('srcaddress')) # this would be a dict of address attributes     
    srcaddress = models.TextField(_('srcaddress')) # this would be a dict of address attributes 
    dstaddress = models.TextField(_('dstaddress')) # this would be a dict of address attributes
    # isprivate = models.BooleanField(_('isprivate'), default=True) # if posted under an offer this would be always set to True, else would be set as False
    isaccepted = models.BooleanField(_('isaccepted'), default=False)
    isnotified = models.BooleanField(_('isnotified'), default=False)
    delivery_code = models.TextField(_('delivery_code'), default='121212')
    ishidden = models.BooleanField(_('ishidden'), default=False)

    def get_delivery_code(self):
        return hashlib.sha256(str(timezone.now()) + str(self.creation_date)).hexdigest()

    def __unicode__(self):
        return str(self.id )

        #Overriding
    def save(self, *args, **kwargs):
        # get a delivery code with 3 letters from the first and 2 from the last
        self.delivery_code = self.get_delivery_code()[:3]+self.get_delivery_code()[-2:]
        super(Quests, self).save(*args, **kwargs)


class QuestComments(models.Model):
    quest = models.ForeignKey(Quests)
    questr = models.ForeignKey(QuestrUserProfile)
    time = models.DateTimeField(_('time'))
    comment = models.TextField(_('comment'))

    def __unicode__(self):
        return self.id