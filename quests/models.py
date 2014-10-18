from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from users.models import *

import logging
import jsonfield
import hashlib
import uuid
logger = logging.getLogger(__name__)


class Quests(models.Model):
    PACKAGE_SELECTION = (('car','Car'),('backpack','Backpack'),('minivan','Minivan'))
    STATUS_SELECTION = (('new','New'),('accepted','Accepted'),('completed','Completed'))

    ## Calculating delivery code before hand and inserting it as default so that it won't be tampered with.
    hashstring = hashlib.sha256(str(timezone.now()) + str(timezone.now()) + str(uuid.uuid4())).hexdigest()
    calc_delivery_code = hashstring[:3]+hashstring[-2:]
    calc_tracking_number = hashstring[10:15]+hashstring[-15:-10]
    current_time = timezone.now

    questrs = models.ForeignKey(QuestrUserProfile)
    # pretty_url = models.CharField(_('pretty_url'), 
    #     max_length=1000, blank=True)
    description = models.TextField(_('description'), blank=True)
    title = models.CharField(_('title'), max_length=100, 
        blank=False)
    reward = models.DecimalField(_('reward'), decimal_places=2, 
        max_digits=1000)
    item_images = models.ImageField(_('item_images'), max_length=9999, upload_to='quest-item-cdn', blank=True)
    map_image = models.URLField(_('map_image'), max_length=9999, default='')
    status = models.TextField(_('status'), choices=STATUS_SELECTION, default='new')
    creation_date = models.DateTimeField(_('creation_date'), 
        default=current_time)
    size = models.TextField(_('size'), choices=PACKAGE_SELECTION, default="backpack")
    shipper = models.TextField(_('shipper'), blank=True, null=True) 
    # qr_code = models.URLField(_('qr_code'), blank=True)
    pickup = jsonfield.JSONField(_('pickup'), default={})
    dropoff = jsonfield.JSONField(_('pickup'), default={})
    isaccepted = models.BooleanField(_('isaccepted'), default=False)
    isnotified = models.BooleanField(_('isnotified'), default=False)
    is_questr_reviewed = models.BooleanField(_('is_questr_reviewed'), default=False)
    is_shipper_reviewed = models.BooleanField(_('is_shipper_reviewed'), default=False)
    is_complete = models.BooleanField(_('is_complete'), default=False)
    ishidden = models.BooleanField(_('ishidden'), default=False)
    distance = models.DecimalField(_('distance'), decimal_places=2,
        max_digits=1000, default=0)
    delivery_date = models.DateTimeField(_('delivery_date'), 
        blank=True, null=True)
    available_couriers = jsonfield.JSONField(_('pickup'), default={})
    delivery_code = models.TextField(_('delivery_code'), blank=True)
    tracking_number = models.TextField(_('tracking_number'), blank=True)
    pickup_time = models.DateTimeField(_('pickup_time'), blank=True)

    def __unicode__(self):
        return str(self.id )

    # def create_item_images_normal(self):
    #     import os
    #     from PIL import Image
    #     from django.core.files.storage import default_storage as storage
    #     if not self.item_images:
    #         logger.debug("No item image")
    #         return ""
    #     file_path = self.item_images.name
    #     logger.debug(file_path)
    #     filename_base, filename_ext = os.path.splitext(file_path)
    #     normal_file_path = "%s_%s_normal.jpg" % (filename_base, self.id)
    #     logger.debug(normal_file_path)
    #     if storage.exists(normal_file_path):
    #         logger.debug("File exists already")
    #         return "exists"
    #     try:
    #         # resize the original image and return url path of the normalnail
    #         f = storage.open(file_path, 'r')
    #         image = Image.open(f)
    #         logger.debug(image)
    #         width, height = image.size
    #         logger.debug(image.size)
    #         if width > height:
    #             delta = width - height
    #             left = int(delta/2)
    #             upper = 0
    #             right = height + left
    #             lower = height
    #         else:
    #             delta = height - width
    #             left = 0
    #             upper = int(delta/2)
    #             right = width
    #             lower = width + upper

    #         image = image.crop((left, upper, right, lower))
    #         image = image.resize((500, 500), Image.ANTIALIAS)

    #         f_normal = storage.open(normal_file_path, "w")
    #         image.save(f_normal, "JPEG")
    #         f_normal.close()
    #         logger.debug("everything went fine")
    #         return "success"
    #     except Exception, e:
    #         logger.debug("error")
    #         logger.debug(e)
    #         return "error"

    # def get_item_images_normal_url(self):
    #     """Returns the url of the aws bucket object"""
    #     from django.core.files.storage import default_storage as storage
    #     default_file_path = "/static/img/default.png"
    #     if not self.item_images:
    #         return default_file_path
    #     normal_file_path = self.item_images.name

    #     ##See if the AWS connection exists or works if doesn't return default file path
    #     try:
    #         if storage.exists(normal_file_path):
    #             # logger.debug(storage.url(normal_file_path))
    #             return storage.url(normal_file_path)
    #     except Exception:
    #         return default_file_path

    #     return default_file_path

    def get_delivery_code(self):
        hashstring = hashlib.sha256(str(timezone.now()) + str(timezone.now()) + str(uuid.uuid4())).hexdigest()
        return hashstring[:3]+hashstring[-2:]

    def get_tracking_number(self): 
        hashstring = hashlib.sha256(str(timezone.now()) + str(timezone.now()) + str(uuid.uuid4())).hexdigest()
        return hashstring[10:15]+hashstring[-15:-10]

        #Overriding
    def save(self, *args, **kwargs):
        if not self.delivery_code:
            self.delivery_code = self.get_delivery_code()

        if not self.tracking_number:
            self.tracking_number = self.get_tracking_number()

        if not self.pickup_time:
            logging.warn("no pickup time")
            self.pickup_time = self.creation_date

        super(Quests, self).save(*args, **kwargs)
        # self.create_item_images_normal()



class QuestComments(models.Model):
    quest = models.ForeignKey(Quests)
    questr = models.ForeignKey(QuestrUserProfile)
    time = models.DateTimeField(_('time'))
    comment = models.TextField(_('comment'))

    def __unicode__(self):
        return self.id

# Quest transactionl model
class QuestTransactional(models.Model):
    id = models.IntegerField(_('id'), primary_key=True)
    quest_code = models.CharField(_('quest_code'), max_length=64, unique=True)
    quest = models.ForeignKey(Quests)
    shipper = models.ForeignKey(QuestrUserProfile)
    transaction_type = models.IntegerField(_('transaction_type'), default=1)
    status = models.BooleanField(_('status'), default=False)

    def generate_hash(self):
        return hashlib.sha256(str(timezone.now()) + str(self.shipper.email)).hexdigest()

    def get_truncated_quest_code(self):
        return self.quest_code[:7]

    def get_token_id(self):
        return self.quest_code[-6:]

    REQUIRED_FIELDS = ['quest_code', 'id', 'quest', 'shipper' ,'transaction_type']

    def __unicode__(self):
        return "{0}:{1} {2}".format(self.quest_code, self.quest, self.shipper)

    #Overriding
    def save(self, *args, **kwargs):
        #check if the row with this hash already exists.
        if not self.quest_code:
            self.quest_code = self.generate_hash()
        # self.my_stuff = 'something I want to save in that field'
        super(QuestTransactional, self).save(*args, **kwargs)

# Questr Token
class QuestToken(models.Model):
    token_id = models.CharField(_('id'), max_length=20, primary_key=True)
    timeframe = models.DateTimeField(_('create_date'), default=timezone.now)

    def is_alive(self):
        timedelta = timezone.now() - self.timeframe
        hours = 2
        allowable_time = float(hours * 60 * 60)
        return timedelta.total_seconds() < allowable_time

    def __unicode__(self):
        return "Token verifying ..."

    # Overriding
    def save(self, *args, **kwargs):
        if not self.timeframe:
            self.timeframe = timezone.now()
        super(QuestToken, self).save(*args, **kwargs)