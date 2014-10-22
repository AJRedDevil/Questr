
from collections import OrderedDict

from django import forms
from django.conf import settings

from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import ugettext_lazy as _
from .models import QuestrUserProfile

class QuestrUserChangeForm(UserChangeForm):
    """
    Form to edit user details, this only changes the general details of the user and not the password
    """
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        for fieldname in ['username']:
            del self.fields['password']
            del self.fields['username']

    CITY_SELECTION = (('Toronto','Toronto'),('Brampton','Brampton'),('Markham','Markham'),
                        ('Mississauga','Mississauga'),('Richmond Hill','Richmond Hill'),('Vaughan','Vaughan'),
                        ('Oakville','Oakville'))
    city = forms.ChoiceField(
        choices=CITY_SELECTION,
        error_messages={
                        'required' : 'Name of the city is required !',
                        'invalid_choice' : 'Please select one of the options available !'
                        }
        )
    streetaddress = forms.CharField(
        error_messages={'required' : 'Street/Apt. Address where the shipment is to be picked up from is required !',}
        )
    streetaddress_2 = forms.CharField(required=False)
    postalcode = forms.CharField(
        error_messages={'required' : 'Your postcode is required !',}
        )
    phone = forms.CharField(required=False)


    class Meta:
        model = QuestrUserProfile
        fields = ['first_name','last_name','displayname','email']
        widgets = {
            'first_name' : forms.TextInput(attrs={'placeholder':'First Name'}),
            'last_name' : forms.TextInput(attrs={'placeholder':'Last Name'}),
            'displayname' : forms.TextInput(attrs={'placeholder':'Your Username'}),
            'email' : forms.TextInput(attrs={'placeholder':'you@example.com'}),
        }
        error_messages = {
            'first_name' : {
                'required' : 'Your first name is required!',
            },
            'last_name' : {
                'required' : 'Your last name is required!',
            },
            'email' : {
                'required' : 'Please provide with a valid email address!',
            },
            'displayname' : {
                'required' : 'You need a username, don\'t you ?',
            },
        }

"""Commented out because we don't have the social signup feature now"""
# class QuestrSocialSignupForm(forms.ModelForm):
#     """
#     This is for when the user signs up with a social account
#     """
#     def __init__(self, *args, **kwargs):
#         super(forms.ModelForm, self).__init__(*args, **kwargs)

#     class Meta:
#         model = QuestrUserProfile
#         fields = ['first_name','last_name','displayname','email']
#         exclude = ('username.help_text',)
#         widgets = {
#             'first_name' : forms.TextInput(attrs={'placeholder':'First Name'}),
#             'last_name' : forms.TextInput(attrs={'placeholder':'Last Name'}),
#             'displayname' : forms.TextInput(attrs={'placeholder':'Your Username'}),
#             'email' : forms.TextInput(attrs={'placeholder':'you@example.com'}),
#         }
#         error_messages = {
#             'first_name' : {
#                 'required' : 'Your first name is required!',
#             },
#             'last_name' : {
#                 'required' : 'Your last name is required!',
#             },
#             'email' : {
#                 'required' : 'Please provide with a valid email address!',
#             },
#             'displayname' : {
#                 'required' : 'You need a username, don\'t you ?',
#             },
#         }



class QuestrUserCreationForm(forms.ModelForm):
    """
    A form that creates a user, from the given data, this runs when the user uses the signup form 
    """
    displayname = forms.RegexField(label=_("Username"), max_length=30,
        regex=r'^[\w.\.+-]+$',
        help_text=_("Required. 30 characters or fewer. Letters, digits and "
                      "./+/-/_ only."),
        error_messages={
            'invalid': _("This value may contain only letters, numbers and "
                         "./+/-/_ characters.")})
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput, min_length=6, 
        error_messages={'required' : 'Please provide with a password !',
                        'min_length' : 'The password has to be more than 6 characters !',
                        })
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput, min_length=6,
        help_text=_("Enter the same password as above, for verification."),
        error_messages={'required' : 'Please provide with a password confirmation !',
                        'min_length' : 'The password has to be more than 6 characters !',
                        })

    CITY_SELECTION = (('Toronto','Toronto'),('Brampton','Brampton'),('Markham','Markham'),
                        ('Mississauga','Mississauga'),('Richmond Hill','Richmond Hill'),('Vaughan','Vaughan'),
                        ('Oakville','Oakville'))
    city = forms.ChoiceField(
        choices=CITY_SELECTION,
        error_messages={
                        'required' : 'Name of the city is required !',
                        'invalid_choice' : 'Please select one of the options available !'
                        }
        )
    streetaddress = forms.CharField(
        error_messages={'required' : 'Street/Apt. Address where the shipment is to be picked up from is required !',}
        )
    streetaddress_2 = forms.CharField(required=False)
    postalcode = forms.CharField(
        error_messages={'required' : 'Your postcode is required !',}
        )
    phone = forms.CharField(required=False)


    error_messages = {
        'password_mismatch': _("The two password fields didn't match. Please re-verify your passwords !"),
        }

    class Meta:
        model = QuestrUserProfile
        fields = ['first_name','last_name','displayname','email','city','postalcode','phone']
        widget = {
            'first_name' : forms.TextInput(attrs = { 'placeholder': 'First Name'}),
            'last_name' : forms.TextInput(attrs = { 'placeholder': 'Last Name'}),
            'email' : forms.TextInput(attrs = { 'placeholder': 'Email Address: me@example.com'}),
            'displayname' : forms.TextInput(attrs = { 'placeholder': 'displayname: Can contain .,+,- OR _'}),
            'password1' : forms.PasswordInput(attrs = { 'placeholder': 'Password'}),
            'password2' : forms.PasswordInput(attrs = { 'placeholder': 'Confirm Password'}),
            'city' : forms.PasswordInput(attrs = { 'placeholder': 'Your City'}),
            'streetaddress' : forms.PasswordInput(attrs = { 'placeholder': 'Your Streeet Address'}),
            'postalcode' : forms.PasswordInput(attrs = { 'placeholder': 'Your Postal Code'}),
            'phone' : forms.PasswordInput(attrs = { 'placeholder': 'Your Phone Number'}),
        }

        error_messages = {
            'first_name' : {
                'required' : 'Your first name is required!',
            },
            'last_name' : {
                'required' : 'Your last name is required!',
            },
            'email' : {
                'required' : 'Please provide with a valid email address!',
            },
            'displayname' : {
                'required' : 'You need a username, don\'t you ?',
            },
            'streetaddress' : {
                'required' : 'Your street address is required',
            },
            'postalcode' : {
                'required' : 'Your postal-code is required',
            },
            'phone' : {
                'required' : 'Your Phone Number is required',
            },
        }

    # def clean_username(self):
    #     # Since User.username is unique, this check is redundant,
    #     # but it sets a nicer error message than the ORM. See #13147.
    #     displayname = self.cleaned_data["displayname"]
    #     try:
    #         QuestrUserProfile._default_manager.get(displayname=displayname)
    #     except QuestrUserProfile.DoesNotExist:
    #         return displayname
    #     raise forms.ValidationError(
    #         self.error_messages['duplicate_username'],
    #         code='duplicate_username',
    #     )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(QuestrUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.avatar_file_name=settings.STATIC_URL+'img/default.png'
        if commit:
            user.save()
        return user

class QuestrLocalAuthenticationForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    username = forms.CharField(label=_("username"),max_length=254)
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    error_messages = {
        'invalid_login': _("Please enter a correct %(username)s and password. "
                           "Note that both fields may be case-sensitive."),
        'inactive': _("This account is inactive, please contact us at hello@questr.co ! "),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super(QuestrLocalAuthenticationForm, self).__init__(*args, **kwargs)

        # Set the label for the "username" field.
        UserModel = get_user_model()
        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        if self.fields['username'].label is None:
            self.fields['username'].label = capfirst(self.username_field.verbose_name)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            elif not self.user_cache.is_active:
                raise forms.ValidationError(
                    self.error_messages['inactive'],
                    code='inactive',
                )
        return self.cleaned_data

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache

class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set his/her password without entering the
    old password
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
        'password1' : {
            'required' : 'Please provide with a password !',
        },
        'password2' : {
            'required' : 'Please provide with a password confirmation !',
        },
    }
    new_password1 = forms.CharField(label=_("New password"),
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=_("New password confirmation"),
                                    widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SetPasswordForm, self).__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
        return self.user


class PasswordChangeForm(SetPasswordForm):
    """
    A form that lets a user change his/her password by entering
    their old password.
    """
    error_messages = dict(SetPasswordForm.error_messages, **{
        'password_incorrect': _("Your old password was entered incorrectly. "
                                "Please enter it again."),
    })
    old_password = forms.CharField(label=_("Old password"),
                                   widget=forms.PasswordInput)

    def clean_old_password(self):
        """
        Validates that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password

PasswordChangeForm.base_fields = OrderedDict(
    (k, PasswordChangeForm.base_fields[k])
    for k in ['old_password', 'new_password1', 'new_password2']
)


class NotifPrefForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(NotifPrefForm, self).__init__(*args, **kwargs)

    PACKAGE_SELECTION = (('car','Car'),('backpack','Backpack'),('minivan','Minivan'))
    NOTIF_SELECTION = (('newquest','Someone posts a new quest'),('applyquest','My posted quests are applied'))

    package = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=PACKAGE_SELECTION)
    notif = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=NOTIF_SELECTION)


