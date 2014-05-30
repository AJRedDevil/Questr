

from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Quests
import logging



class QuestCreationForm(forms.ModelForm):
    """
    A form that creates a post, from the given data
    """
    class Meta:
        model = Quests
        exclude = ['questrs','status','creation_date','is_accepted','pretty_url','location',]
        widget = {
            'title' : forms.TextInput(attrs = { 'placeholder': 'Title'}),
            'reward' : forms.TextInput(attrs = { 'placeholder': "You're offering"}),            
            'location' : forms.TextInput(attrs = { 'placeholder': "Location"}),
            'srcaddress' : forms.TextInput(attrs = { 'placeholder': "Departure Address"}),
            'dstaddress' : forms.TextInput(attrs = { 'placeholder': "Destination Address"}),
            'description' : forms.TextInput(attrs = { 'placeholder': "Description"}),
            'item_images' : forms.TextInput(attrs = { 'placeholder': "Image"}),
        }
