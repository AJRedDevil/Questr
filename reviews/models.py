from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from users.model import QuestrUserProfile
from quests.model import Quests

# Create your models here.

class Questr(models.Model):
    """docstring for questr"""
    id = models.ForeignKey(QuestrUserProfile)
    quest = models.ForeignKey(Quests)
    reviewer = models.ForeignKey(QuestrUserProfile)
    rating_1 = models.DecimalField(_('rating_1'), default='0', max_digits=5, decimal_places=2)
    rating_2 = models.DecimalField(_('rating_2'), default='0', max_digits=5, decimal_places=2)
    rating_3 = models.DecimalField(_('rating_3'), default='0', max_digits=5, decimal_places=2)
    rating_4 = models.DecimalField(_('rating_4'), default='0', max_digits=5, decimal_places=2)
    rating_5 = models.DecimalField(_('rating_5'), default='0', max_digits=5, decimal_places=2)
    final_rating = models.DecimalField(_('final_rating'), default='0', max_digits=5, decimal_places=2)
    review = models.TextField(_('review'), default=None)

    def __unicode__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        self.final_rating = (float(self.rating_1)+float(self.rating_2)+float(self.rating_3)+float(self.rating_4)+float(self.rating_5))/5G
        super(Questr, self).save(*args, **kwargs)