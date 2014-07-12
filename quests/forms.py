

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
        exclude = ['questrs','status','creation_date','is_accepted', 'shipper', 'delivery_code', 'reward']
        # widget = {
        #     'title' : forms.TextInput(attrs = { 'placeholder': 'Title'}),
        #     'reward' : forms.TextInput(attrs = { 'placeholder': "You're offering"}),            
        #     'Package Type' : forms.RadioSelect(attrs = { 'default': "1"}),
        #     'srcaddress' : forms.TextInput(attrs = { 'placeholder': "Departure Address"}),
        #     'dstaddress' : forms.TextInput(attrs = { 'placeholder': "Destination Address"}),
        #     'srccity' : forms.TextInput(attrs = { 'placeholder': "Departure City"}),
        #     'dstcity' : forms.TextInput(attrs = { 'placeholder': "Destination City"}),
        #     'description' : forms.TextInput(attrs = { 'placeholder': "Description"}),
        #     'item_images' : forms.TextInput(attrs = { 'placeholder': "Image"}),
        # }

class QuestChangeForm(forms.ModelForm):
    """
    A form that creates a post, from the given data
    """
    class Meta:
        model = Quests
        exclude = ['questrs','status','creation_date','is_accepted', 'shipper', 'delivery_code', 'reward']
        # widget = {
        #     'title' : forms.TextInput(attrs = { 'placeholder': 'Title'}),
        #     'reward' : forms.TextInput(attrs = { 'placeholder': "You're offering"}),            
        #     'location' : forms.TextInput(attrs = { 'placeholder': "Location"}),
        #     'srcaddress' : forms.TextInput(attrs = { 'placeholder': "Departure Address"}),
        #     'dstaddress' : forms.TextInput(attrs = { 'placeholder': "Destination Address"}),
        #     'srccity' : forms.TextInput(attrs = { 'placeholder': "Departure City"}),
        #     'dstcity' : forms.TextInput(attrs = { 'placeholder': "Destination City"}),
        #     'description' : forms.TextInput(attrs = { 'placeholder': "Description"}),
        #     'item_images' : forms.TextInput(attrs = { 'placeholder': "Image"}),
        # }