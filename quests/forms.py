

from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Quests
import logging



class QuestCreationForm(forms.ModelForm):
    """
    A form that creates a post, from the given data
    """
    CITY_SELECTION = (('Toronto','Toronto'),('Brampton','Brampton'),('Markham','Markham'),
                        ('Mississauga','Mississauga'),('Richmond Hill','Richmond Hill'),('Vaughan','Vaughan'))
    srccity = forms.ChoiceField(
        choices=CITY_SELECTION,
        error_messages={
                        'required' : 'Name of the city is required !',
                        'invalid_choice' : 'Please select one of the options available !'
                        }
        )
    srcaddress = forms.CharField(
        error_messages={'required' : 'Street/Apt. Address where the shipment is to be picked up from is required !',}
        )
    srcname = forms.CharField(
        error_messages={'required' : 'Name of the sender is required!',}
        )
    srcphone = forms.CharField(required=False)
    srcpostalcode = forms.CharField(
        error_messages={'required' : 'Your postcode is required !',}
        )
    dstcity = forms.ChoiceField(
        choices=CITY_SELECTION,
        error_messages={'required' : 'Name of the city is required !',
                        'invalid_choice' : 'Please select one of the options available !',
                        }
        )
    dstaddress = forms.CharField(
        error_messages={'required' : 'Street/Apt. Address where the shipment is to be picked up from is required !',}
        )
    dstname = forms.CharField(
        error_messages={'required' : 'Name of the sender is required!',}
        )
    dstphone = forms.CharField(required=False)
    dstpostalcode = forms.CharField(
        error_messages={'required' : 'Your postcode is required !',}
        )
    class Meta:
        model = Quests
        exclude = ['questrs','status','creation_date','is_accepted', 'shipper', 'delivery_code', 'reward', \
            'item_images', 'distance', 'pickup', 'dropoff', 'delivery_date']
        widget = {
            'description' : forms.TextInput(attrs = { 'placeholder': "Description"}),
            'title' : forms.TextInput(attrs = { 'placeholder': 'Title'}),
            'size' : forms.RadioSelect(attrs = { 'default': "backpack"}),
            'srccity' : forms.Select(attrs = { 'placeholder': "toronto"}),
            'srcaddress' : forms.TextInput(attrs = { 'placeholder': "Departure Address"}),
            'srcname' : forms.TextInput(attrs = { 'placeholder': "John Doe"}),
            'srcphone' : forms.TextInput(attrs = { 'placeholder': "+111-222-333"}),
            'srcpostal' : forms.TextInput(attrs = { 'placeholder': "+111-222-333"}),
            'dstcity' : forms.Select(attrs = { 'placeholder': "toronto"}),
            'dstaddress' : forms.TextInput(attrs = { 'placeholder': "Delivery Address"}),
            'dstname' : forms.TextInput(attrs = { 'placeholder': "John Doe"}),
            'dstphone' : forms.TextInput(attrs = { 'placeholder': "+111-222-333"}),
            'dstpostalcode' : forms.TextInput(attrs = { 'placeholder': "+111-222-333"}),
        }
        error_messages = {
            'size' : {
                'required' : 'We need to know how you like your item to be shipped!',
                'invalid_choice' : 'Please select one of the options available !',
            },
            'title' : {
                'required' : 'A title is required !',
            },
        }

class QuestConfirmForm(forms.ModelForm):
    """
    A form that creates a post, from the given data
    """
    CITY_SELECTION = (('Toronto','Toronto'),('Brampton','Brampton'),('Markham','Markham'),
                        ('Mississauga','Mississauga'),('Richmond Hill','Richmond Hill'),('Vaughan','Vaughan'))
    srccity = forms.ChoiceField(
        choices=CITY_SELECTION,
        error_messages={
                        'required' : 'Name of the city is required !',
                        'invalid_choice' : 'Please select one of the options available !'
                        }
        )
    srcaddress = forms.CharField(
        error_messages={'required' : 'Street/Apt. Address where the shipment is to be picked up from is required !',}
        )
    srcname = forms.CharField(
        error_messages={'required' : 'Name of the sender is required!',}
        )
    srcphone = forms.CharField(required=False)
    srcpostalcode = forms.CharField(
        error_messages={'required' : 'Your postcode is required !',}
        )
    dstcity = forms.ChoiceField(
        choices=CITY_SELECTION,
        error_messages={'required' : 'Name of the city is required !',
                        'invalid_choice' : 'Please select one of the options available !',
                        }
        )
    dstaddress = forms.CharField(
        error_messages={'required' : 'Street/Apt. Address where the shipment is to be picked up from is required !',}
        )
    dstname = forms.CharField(
        error_messages={'required' : 'Name of the sender is required!',}
        )
    dstphone = forms.CharField(required=False)
    dstpostalcode = forms.CharField(
        error_messages={'required' : 'Your postcode is required !',}
        )
    class Meta:
        model = Quests
        exclude = ['questrs','status','creation_date','is_accepted', 'shipper', 'delivery_code', 'pickup', \
            'dropoff', 'delivery_date']
        widget = {
            'description' : forms.TextInput(attrs = { 'placeholder': "Description"}),
            'title' : forms.TextInput(attrs = { 'placeholder': 'Title'}),
            'reward' : forms.NumberInput(attrs = { 'placeholder': 'You Pay'}),
            'size' : forms.RadioSelect(attrs = { 'default': "backpack"}),
            'srccity' : forms.Select(attrs = { 'placeholder': "toronto"}),
            'srcaddress' : forms.TextInput(attrs = { 'placeholder': "Departure Address"}),
            'srcname' : forms.TextInput(attrs = { 'placeholder': "John Doe"}),
            'srcphone' : forms.TextInput(attrs = { 'placeholder': "+111-222-333"}),
            'srcpostal' : forms.TextInput(attrs = { 'placeholder': "+111-222-333"}),
            'dstcity' : forms.Select(attrs = { 'placeholder': "toronto"}),
            'dstaddress' : forms.TextInput(attrs = { 'placeholder': "Delivery Address"}),
            'dstname' : forms.TextInput(attrs = { 'placeholder': "John Doe"}),
            'dstphone' : forms.TextInput(attrs = { 'placeholder': "+111-222-333"}),
            'dstpostalcode' : forms.TextInput(attrs = { 'placeholder': "+111-222-333"}),
        }
        error_messages = {
            'size' : {
                'required' : 'We need to know how you like your item to be shipped!',
                'invalid_choice' : 'Please select one of the options available !',
            },
            'title' : {
                'required' : 'A title is required !',
            },
            'reward' : {
                'required' : 'Every shipment has a price!',
                'invalid' : 'There is a limit to how much one pays for a shipment!',
            },

        }

class QuestChangeForm(forms.ModelForm):
    """
    A form to edit a quest that has been created already
    """
    CITY_SELECTION = (('Toronto','Toronto'),('Brampton','Brampton'),('Markham','Markham'),
                        ('Mississauga','Mississauga'),('Richmond Hill','Richmond Hill'),('Vaughan','Vaughan'))
    srccity = forms.ChoiceField(
        choices=CITY_SELECTION,
        error_messages={
                        'required' : 'Name of the city is required !',
                        'invalid_choice' : 'Please select one of the options available !'
                        }
        )
    srcaddress = forms.CharField(
        error_messages={'required' : 'Street/Apt. Address where the shipment is to be picked up from is required !',}
        )
    srcname = forms.CharField(
        error_messages={'required' : 'Name of the sender is required!',}
        )
    srcphone = forms.CharField(required=False)
    srcpostalcode = forms.CharField(
        error_messages={'required' : 'Your postcode is required !',}
        )
    dstcity = forms.ChoiceField(
        choices=CITY_SELECTION,
        error_messages={'required' : 'Name of the city is required !',
                        'invalid_choice' : 'Please select one of the options available !',
                        }
        )
    dstaddress = forms.CharField(
        error_messages={'required' : 'Street/Apt. Address where the shipment is to be picked up from is required !',}
        )
    dstname = forms.CharField(
        error_messages={'required' : 'Name of the sender is required!',}
        )
    dstphone = forms.CharField(required=False)
    dstpostalcode = forms.CharField(
        error_messages={'required' : 'Your postcode is required !',}
        )
    class Meta:
        model = Quests
        exclude = ['questrs','reward','status','creation_date','is_accepted', 'shipper', 'distance', 'delivery_code',  \
            'item_images', 'pickup', 'dropoff', 'delivery_date']

        widget = {
            'description' : forms.TextInput(attrs = { 'placeholder': "Description"}),
            'title' : forms.TextInput(attrs = { 'placeholder': 'Title'}),
            'size' : forms.RadioSelect(attrs = { 'default': "backpack"}),
            'srccity' : forms.Select(attrs = { 'placeholder': "toronto"}),
            'srcaddress' : forms.TextInput(attrs = { 'placeholder': "Departure Address"}),
            'srcname' : forms.TextInput(attrs = { 'placeholder': "John Doe"}),
            'srcphone' : forms.TextInput(attrs = { 'placeholder': "+111-222-333"}),
            'srcpostal' : forms.TextInput(attrs = { 'placeholder': "+111-222-333"}),
            'dstcity' : forms.Select(attrs = { 'placeholder': "toronto"}),
            'dstaddress' : forms.TextInput(attrs = { 'placeholder': "Delivery Address"}),
            'dstname' : forms.TextInput(attrs = { 'placeholder': "John Doe"}),
            'dstphone' : forms.TextInput(attrs = { 'placeholder': "+111-222-333"}),
            'dstpostalcode' : forms.TextInput(attrs = { 'placeholder': "+111-222-333"}),
        }
        error_messages = {
            'size' : {
                'required' : 'We need to know how you like your item to be shipped!',
                'invalid_choice' : 'Please select one of the options available !',
            },
            'title' : {
                'required' : 'A title is required !',
            },
        }