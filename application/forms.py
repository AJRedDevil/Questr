from django import forms
from django.utils.translation import ugettext_lazy as _

PHONE_TYPES = (
    ('ios', 'iOS'),
    ('android', 'Android'),
    ('others', 'Others')
)
BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))
ACCESSIBILITY_CHOICES = (('yes', 'Yes'), ('no', 'No'), ('others', 'Others'))
VEHICLE_TYPES = (
    ('coupe', 'Coupe'),
    ('minivan', 'Minivan'),
    ('pickup', 'Pickup'),
    ('sedan', 'Sedan'),
    ('suv', 'SUV'),
    ('van', 'Van'),
    ('wagen', 'Wagen'),
    ('hatchback', 'Hatchback of any kind'),
    ('other', 'Other'),
)
LICENSE_TYPES = (
    ('G', 'G'),
    ('M', 'M'),
    ('G2', 'G2')
)
DAYS = (
    ('monday', 'Monday'),
    ('tuesday', 'Tuesday'),
    ('wednesday', 'Wednesday'),
    ('thursday', 'Thursday'),
    ('friday', 'Friday'),
    ('saturday', 'Saturday'),
    ('sunday', 'Sunday'),
)
HOURS = (
    ('00000559', '00:00 - 05:59'),
    ('06001159', '06:00 - 11:59'),
    ('12001759', '12:00 - 17:59'),
    ('18002359', '18:00 - 23:59'),
)
REGULAR_DELIVERY = {
    ('1-10', '1~10/month'),
    ('11-30', '11~30/month'),
    ('31', '31+/month'),
}
AVG_PKG_SIZE = {
    ('envelope','Documents, prints'),
    ('box','Items that can fit in a moving box'),
    ('grande','Items larger (or longer, wider) than a moving box'),
}

class CourierApplyForm(forms.Form):
    """
    Forms for couriers to apply for job
    """
    name = forms.CharField(
        label=_('Name'),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'John Smith',
            }
        ),
        error_messages={
            'required': _('Name is required!')
        }
    )
    email = forms.CharField(
        label=_('Email'),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'johnsmitty@example.com',
            }
        ),
        error_messages={
            'required': _('Email is required!')
        }
    )
    phone = forms.CharField(
        label=_('Phone'),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '123-456-7890'
            }
        ),
        error_messages={
            'required': _('Phone is required!')
        }
    )
    postalcode = forms.CharField(
        label=_('Postalcode'),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'M1A 2B3'
            }
        ),
        error_messages={
            'required': _('Name is required!')
        }
    )
    phone_type = forms.ChoiceField(
        choices=PHONE_TYPES,
        widget=forms.RadioSelect(),
        error_messages={
            'required': _('Type of phone is required!')
        }
    )
    ios_accessible = forms.BooleanField(
        widget=forms.RadioSelect(
            choices=BOOL_CHOICES,
        ),
        error_messages={
            'required': _('Please state a choice!')
        }
    )
    car_accessible = forms.ChoiceField(
        choices=ACCESSIBILITY_CHOICES,
        widget=forms.RadioSelect(),
        error_messages={
            'required': _('This field is required!')
        }
    )
    vehicle_type = forms.ChoiceField(
        choices=VEHICLE_TYPES,
        widget=forms.Select(),
        error_messages={
            'required': _('This field is required!')
        }
    )
    backseats_down = forms.ChoiceField(
        choices=BOOL_CHOICES,
        widget=forms.RadioSelect(),
        error_messages={
            'required': _('This field is required!')
        }
    )
    license_type = forms.ChoiceField(
        choices=LICENSE_TYPES,
        widget=forms.RadioSelect(),
        error_messages={
            'required': _('This field is required!')
        }
    )
    available_days = forms.MultipleChoiceField(
        choices=DAYS,
        widget=forms.CheckboxSelectMultiple,
        error_messages={
            'required': _('This field is required!')
        }
    )
    available_hours = forms.MultipleChoiceField(
        choices=HOURS,
        widget=forms.CheckboxSelectMultiple,
        error_messages={
            'required': _('This field is required!')
        }
    )
    fulltime_or_parttime = forms.BooleanField(
        widget=forms.RadioSelect(
            choices=BOOL_CHOICES,
            attrs={'class': 'form-control'}
        ),
        error_messages={
            'required': _('This field is required!')
        }
    )
    previous_job = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'If fulltime what was your previous job?'
            }
        ),
        error_messages={
            'required': _('This field is required!')
        }
    )
    other_job = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'If part time what is your other job?'
            }
        ),
        error_messages={
            'required': _('This field is required!')
        }
    )
    accessibility_permit = forms.ChoiceField(
        choices=ACCESSIBILITY_CHOICES,
        widget=forms.RadioSelect(),
        error_messages={
            'required': _('This field is required!')
        }
    )

class UserApplyForm(forms.Form):
    """
    Forms for users to request invites
    """
    name = forms.CharField(
        label=_('Name'),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'John Smith',
            }
        ),
        error_messages={
            'required': _('Name is required!')
        }
    )
    email = forms.CharField(
        label=_('Email'),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'johnsmitty@example.com',
            }
        ),
        error_messages={
            'required': _('Email is required!')
        }
    )
    phone = forms.CharField(
        label=_('Phone'),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '123-456-7890'
            }
        ),
        error_messages={
            'required': _('Phone is required!')
        }
    )
    postalcode = forms.CharField(
        label=_('Postalcode'),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'M1A 2B3'
            }
        ),
        error_messages={
            'required': _('Postal code is required!')
        }
    )
    regular_delivery = forms.ChoiceField(
        choices=REGULAR_DELIVERY,
        widget=forms.RadioSelect(),
        error_messages={
            'required': _('This field is required!')
        }
    )

    avg_pkg_size = forms.ChoiceField(
        choices=AVG_PKG_SIZE,
        widget=forms.RadioSelect(),
        error_messages={
            'required': _('This field is required!')
        }
    )

    msg = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Anything you would like to share with us.'
            }
        ),
        error_messages={
            'required': _('This field is required!')
        }
    )
