
from django import forms
from .models import Quests, PACKAGE_SELECTION


class QuestCreationForm(forms.ModelForm):
    """
    A form that creates a post, from the given data
    """
    CITY_SELECTION = (
        ('Toronto', 'Toronto'),
        ('Brampton', 'Brampton'),
        ('Markham', 'Markham'),
        ('Mississauga', 'Mississauga'),
        ('Richmond Hill', 'Richmond Hill'),
        ('Vaughan', 'Vaughan'),
        ('Oakville', 'Oakville')
    )

    size = forms.ChoiceField(
        choices=PACKAGE_SELECTION,
        error_messages={
            'required': 'We need to know how you like your item to be shipped!',
            'invalid_choice': 'Please select one of the options available !',
        },
        widget=forms.Select(
            attrs={
                'class': 'form-control m-b',
                'required': 'true'
            }
        )
    )

    srccity = forms.ChoiceField(
        choices=CITY_SELECTION,
        error_messages={
            'required': 'Name of the city is required !',
            'invalid_choice': 'Please select one of the options available !'
        },
        widget=forms.Select(
            attrs={
                'class': 'form-control input-lg',
                'data-size': '5',
                'required': 'true'
            }
        )
    )

    srcaddress = forms.CharField(
        error_messages={
            'required': 'Street/Apt. Address where the \
            shipment is to be picked up from is required !',
        },
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-lg',
                'placeholder': 'Street Address, P.O box, company name, etc',
                'required': 'true'
            }
        )
    )

    srcaddress_2 = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-lg',
                'placeholder': 'Apartment, suite, unit, building, floor, etc.',
                'required': 'false'
            }
        )
    )

    srcname = forms.CharField(
        error_messages={
            'required': 'Name of the sender is required!',
        },
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-lg',
                'placeholder': 'John Doe',
                'required': 'true'
            }
        )
    )

    srcphone = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-lg',
                'data-mask': '(999) 999-9999',
                'placeholder': '(123) 456 - 7890',
                'required': 'true'
            }
        )
    )

    srcpostalcode = forms.CharField(
        error_messages={
            'required': 'Your postcode is required !',
        },
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-lg',
                'placeholder': 'M8V 0A5',
                'required': 'true',
            }
        )
    )

    dstcity = forms.ChoiceField(
        choices=CITY_SELECTION,
        error_messages={
            'required': 'Name of the city is required !',
            'invalid_choice': 'Please select one of the options available !'
        },
        widget=forms.Select(
            attrs={
                'class': 'form-control input-lg',
                'data-size': '5',
                'required': 'true',
            }
        )
    )

    dstaddress = forms.CharField(
        error_messages={
            'required': 'Street/Apt. Address where the \
            shipment is to be dropped off from is required !',
        },
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-lg',
                'placeholder': 'Street Address, P.O box, company name, etc',
                'required': 'true',
            }
        )
    )

    dstaddress_2 = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-lg',
                'placeholder': 'Apartment, suite, unit, building, floor, etc.',
            }
        )
    )

    dstname = forms.CharField(
        error_messages={
            'required': 'Name of the receiver is required!',
        },
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-lg',
                'placeholder': 'John Doe',
                'required': 'true',
            }
        )
    )

    dstphone = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-lg',
                'data-mask': '(999) 999-9999',
                'placeholder': '(123) 456 - 7890',
                'required': 'true',
            }
        )
    )

    dstpostalcode = forms.CharField(
        error_messages={
            'required': 'Your postcode is required !',
        },
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-lg',
                'placeholder': 'M8V 0A5',
                'required': 'true',
            }
        )
    )

    class Meta:
        model = Quests
        fields = ['title', 'size', 'description']

    def __init__(self, *args, **kwargs):
        super(QuestCreationForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs = {
            'class': 'form-control input-lg',
            'required': 'true',
            'placeholder': 'Name of your shipment.'
        }
        self.fields['description'].widget.attrs = {
            'class': 'form-control',
            'rows': '5',
            'required': 'true',
            'placeholder': 'Tell us about your shipment.'
        }


class QuestConfirmForm(forms.ModelForm):
    """
    A form that creates a post, from the given data
    """
    CITY_SELECTION = (
        ('Toronto', 'Toronto'),
        ('Brampton', 'Brampton'),
        ('Markham', 'Markham'),
        ('Mississauga', 'Mississauga'),
        ('Richmond Hill', 'Richmond Hill'),
        ('Vaughan', 'Vaughan'),
        ('Oakville', 'Oakville')
    )

    size = forms.ChoiceField(
        choices=PACKAGE_SELECTION,
        error_messages={
            'required': 'We need to know how you like your item to be shipped!',
            'invalid_choice': 'Please select one of the options available !',
        },
    )

    srccity = forms.ChoiceField(
        choices=CITY_SELECTION,
        error_messages={
            'required': 'Name of the city is required !',
            'invalid_choice': 'Please select one of the options available !'
        },
    )

    srcaddress = forms.CharField(
        error_messages={
            'required': 'Street/Apt. Address where the \
            shipment is to be picked up from is required !',
        },
    )

    srcaddress_2 = forms.CharField(
        required=False,
    )

    srcname = forms.CharField(
        error_messages={
            'required': 'Name of the sender is required!',
        },
    )

    srcphone = forms.CharField(
        required=False,
    )

    srcpostalcode = forms.CharField(
        error_messages={
            'required': 'Your postcode is required !',
        },
    )

    dstcity = forms.ChoiceField(
        choices=CITY_SELECTION,
        error_messages={
            'required': 'Name of the city is required !',
            'invalid_choice': 'Please select one of the options available !'
        },
    )

    dstaddress = forms.CharField(
        error_messages={
            'required': 'Street/Apt. Address where the \
            shipment is to be dropped off from is required !',
        },
    )

    dstaddress_2 = forms.CharField(
        required=False,
    )

    dstname = forms.CharField(
        error_messages={
            'required': 'Name of the receiver is required!',
        },
    )

    dstphone = forms.CharField(
        required=False,
    )

    dstpostalcode = forms.CharField(
        error_messages={
            'required': 'Your postcode is required !',
        },
    )

    # PICKUP_TIME_SELECTION = (('now','Now'),('not_now','Not_now'))
    # NOT_NOW_SELECTION = (('Today','Today'),('Tomorrow','Tomorrow'))

    # pickup_time = forms.ChoiceField(choices=PICKUP_TIME_SELECTION, widget=forms.RadioSelect())
    # pickup_when = forms.ChoiceField(required=False,
    #     choices=NOT_NOW_SELECTION, 
    #     error_messages={
    #                     'invalid_choice' : 'Please select one of the options available !'
    #                     })
    # not_now_pickup_time = forms.CharField(required=False)

    class Meta:
        model = Quests
        exclude = ['questrs','status','creation_date','isaccepted', 'shipper', 'delivery_code', 'pickup', \
            'dropoff', 'delivery_date', 'map_image','available_couriers','tracking_number', 'pickup_time','considered_couriers']

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

# class QuestChangeForm(forms.ModelForm):
#     """
#     A form to edit a quest that has been created already
#     """
#     CITY_SELECTION = (('Toronto','Toronto'),('Brampton','Brampton'),('Markham','Markham'),
#                         ('Mississauga','Mississauga'),('Richmond Hill','Richmond Hill'),('Vaughan','Vaughan'),
#                         ('Oakville','Oakville'))
#     srccity = forms.ChoiceField(
#         choices=CITY_SELECTION,
#         error_messages={
#                         'required' : 'Name of the city is required !',
#                         'invalid_choice' : 'Please select one of the options available !'
#                         }
#         )
#     srcaddress = forms.CharField(
#         error_messages={'required' : 'Street/Apt. Address where the shipment is to be picked up from is required !',}
#         )
#     srcname = forms.CharField(
#         error_messages={'required' : 'Name of the sender is required!',}
#         )
#     srcphone = forms.CharField(required=False)
#     srcpostalcode = forms.CharField(
#         error_messages={'required' : 'Your postcode is required !',}
#         )
#     dstcity = forms.ChoiceField(
#         choices=CITY_SELECTION,
#         error_messages={'required' : 'Name of the city is required !',
#                         'invalid_choice' : 'Please select one of the options available !',
#                         }
#         )
#     dstaddress = forms.CharField(
#         error_messages={'required' : 'Street/Apt. Address where the shipment is to be picked up from is required !',}
#         )
#     dstname = forms.CharField(
#         error_messages={'required' : 'Name of the sender is required!',}
#         )
#     dstphone = forms.CharField(required=False)
#     dstpostalcode = forms.CharField(
#         error_messages={'required' : 'Your postcode is required !',}
#         )
#     class Meta:
#         model = Quests
#         exclude = ['questrs','reward','status','creation_date','isaccepted', 'shipper', 'distance', 'delivery_code',  \
#             'item_images', 'pickup', 'dropoff', 'delivery_date', 'map_image','available_couriers','tracking_number']

#         widget = {
#             'description' : forms.TextInput(attrs = { 'placeholder': "Description"}),
#             'title' : forms.TextInput(attrs = { 'placeholder': 'Title'}),
#             'size' : forms.RadioSelect(attrs = { 'default': "backpack"}),
#             'srccity' : forms.Select(attrs = { 'placeholder': "toronto"}),
#             'srcaddress' : forms.TextInput(attrs = { 'placeholder': "Departure Address"}),
#             'srcname' : forms.TextInput(attrs = { 'placeholder': "John Doe"}),
#             'srcphone' : forms.TextInput(attrs = { 'placeholder': "+111-222-333"}),
#             'srcpostal' : forms.TextInput(attrs = { 'placeholder': "+111-222-333"}),
#             'dstcity' : forms.Select(attrs = { 'placeholder': "toronto"}),
#             'dstaddress' : forms.TextInput(attrs = { 'placeholder': "Delivery Address"}),
#             'dstname' : forms.TextInput(attrs = { 'placeholder': "John Doe"}),
#             'dstphone' : forms.TextInput(attrs = { 'placeholder': "+111-222-333"}),
#             'dstpostalcode' : forms.TextInput(attrs = { 'placeholder': "+111-222-333"}),
#         }
#         error_messages = {
#             'size' : {
#                 'required' : 'We need to know how you like your item to be shipped!',
#                 'invalid_choice' : 'Please select one of the options available !',
#             },
#             'title' : {
#                 'required' : 'A title is required !',
#             },
#         }

class DistancePriceForm(forms.Form):
    """
    A form to get distance relative information 
    """
    def __init__(self, *args, **kwargs):
        super(DistancePriceForm, self).__init__(*args, **kwargs)

    CITY_SELECTION = (('Toronto','Toronto'),('Brampton','Brampton'),('Markham','Markham'),
                        ('Mississauga','Mississauga'),('Richmond Hill','Richmond Hill'),('Vaughan','Vaughan'),
                        ('Oakville','Oakville'))
    PACKAGE_SELECTION = (('car','Car'),('backpack','Backpack'),('minivan','Minivan'))

    srccity = forms.ChoiceField(
        choices=CITY_SELECTION,
        error_messages={
                        'required' : 'Name of the city is required !',
                        'invalid_choice' : 'Please select one of the options available !'
                        }
        )
    size = forms.ChoiceField(
        choices=PACKAGE_SELECTION,
        error_messages={'required' : 'We need to know how you like your item to be shipped!',
                        'invalid_choice' : 'Please select one of the options available !',
                        }
        )
    srcaddress = forms.CharField(
        error_messages={'required' : 'Street/Apt. Address where the shipment is to be picked up from is required !',}
        )
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
    dstpostalcode = forms.CharField(
        error_messages={'required' : 'Your postcode is required !',}
        )

class TrackingNumberSearchForm(forms.Form):
    """A form to get details of the shipment from the tracking number"""
    def __init__(self, *args, **kwargs):
        super(TrackingNumberSearchForm, self).__init__(*args, **kwargs)

    tracking_number = forms.CharField(
        error_messages = {'required':'Please provide with a tracking number'}
        )
