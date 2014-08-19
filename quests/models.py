from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from users.models import *

import logging
import jsonfield

class Quests(models.Model):
    questrs = models.ForeignKey(QuestrUserProfile)
    # pretty_url = models.CharField(_('pretty_url'), 
    #     max_length=1000, blank=True)
    description = models.TextField(_('description'))
    title = models.CharField(_('title'), max_length=100, 
        blank=False)
    reward = models.DecimalField(_('reward'), decimal_places=2, 
        max_digits=1000)
    item_images = models.ImageField(_('item_images'), max_length=9999, upload_to='quest-item-cdn', blank=True)
    status = models.TextField(_('status'), default='new')
    creation_date = models.DateTimeField(_('creation_date'), 
        blank=False)
    size = models.TextField(_('size'), default="backpack")
    shipper = models.TextField(_('shipper'), blank=True, null=True) # if posted under an offer this would be a single digit (pk of questr object of the offerer)
    # qr_code = models.URLField(_('qr_code'), blank=True)
    pickup = jsonfield.JSONField(_('pickup'), default={})
    dropoff = jsonfield.JSONField(_('pickup'), default={})
    isaccepted = models.BooleanField(_('isaccepted'), default=False)
    isnotified = models.BooleanField(_('isnotified'), default=False)
    is_questr_reviewed = models.BooleanField(_('is_questr_reviewed'), default=False)
    is_shipper_reviewed = models.BooleanField(_('is_shipper_reviewed'), default=False)
    is_complete = models.BooleanField(_('is_complete'), default=False)
    delivery_code = models.TextField(_('delivery_code'), default='121212')
    ishidden = models.BooleanField(_('ishidden'), default=False)
    distance = models.DecimalField(_('distance'), decimal_places=2,
        max_digits=1000, default=0)
    delivery_date = models.DateTimeField(_('delivery_date'), 
        blank=True, null=True)

    def get_delivery_code(self):
        return hashlib.sha256(str(timezone.now()) + str(self.creation_date)).hexdigest()

    def __unicode__(self):
        return str(self.id )

    def create_item_images_normal(self):
        import os
        from PIL import Image
        from django.core.files.storage import default_storage as storage
        if not self.item_images:
            logging.warn("No item image")
            return ""
        file_path = self.item_images.name
        logging.warn(file_path)
        filename_base, filename_ext = os.path.splitext(file_path)
        normal_file_path = "%s_%s_normal.jpg" % (filename_base, self.id)
        logging.warn(normal_file_path)
        if storage.exists(normal_file_path):
            logging.warn("File exists already")
            return "exists"
        try:
            # resize the original image and return url path of the normalnail
            f = storage.open(file_path, 'r')
            image = Image.open(f)
            logging.warn(image)
            width, height = image.size
            logging.warn(image.size)
            if width > height:
                delta = width - height
                left = int(delta/2)
                upper = 0
                right = height + left
                lower = height
            else:
                delta = height - width
                left = 0
                upper = int(delta/2)
                right = width
                lower = width + upper

            image = image.crop((left, upper, right, lower))
            image = image.resize((500, 500), Image.ANTIALIAS)

            f_normal = storage.open(normal_file_path, "w")
            image.save(f_normal, "JPEG")
            f_normal.close()
            logging.warn("everything went fine")
            return "success"
        except Exception, e:
            logging.warn("error")
            logging.warn(e)
            return "error"

    def get_item_images_normal_url(self):
        """Returns the url of the aws bucket object"""
        import os
        from django.core.files.storage import default_storage as storage
        default_file_path = "/static/img/default.png"
        if not self.item_images:
            return default_file_path
        normal_file_path = self.item_images.name

        ##See if the AWS connection exists or works if doesn't return default file path
        try:
            if storage.exists(normal_file_path):
                # logging.warn(storage.url(normal_file_path))
                return storage.url(normal_file_path)
        except Exception, e:
            return default_file_path

        return default_file_path


        #Overriding
    def save(self, *args, **kwargs):
        # get a delivery code with 3 letters from the first and 2 from the last
        if self.delivery_code=='121212':
            self.delivery_code = self.get_delivery_code()[:3]+self.get_delivery_code()[-2:]
        super(Quests, self).save(*args, **kwargs)
        self.create_item_images_normal()



class QuestComments(models.Model):
    quest = models.ForeignKey(Quests)
    questr = models.ForeignKey(QuestrUserProfile)
    time = models.DateTimeField(_('time'))
    comment = models.TextField(_('comment'))

    def __unicode__(self):
        return self.id