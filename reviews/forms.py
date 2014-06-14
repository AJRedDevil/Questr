

from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Quests
import logging



class ReviewForm(forms.ModelForm):
    """
    A form that creates a post, from the given data
    """
    class Meta:
        model = Questr
        exclude = ['id','quest','reviewer','final_rating']