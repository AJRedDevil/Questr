from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import ugettext_lazy as _
from .models import QuestrUserProfile
import logging

class QuestrUserChangeForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        for fieldname in ['username']:
            self.fields[fieldname].help_text = None
            del self.fields['password']

            #changed label for form items
        self.fields['privacy'].label = "Privacy"
        self.fields['biography'].label = "Your biography"

    class Meta:
        model = QuestrUserProfile
        fields = ['first_name','last_name','username','email','phone','biography','privacy']
        exclude = ('username.help_text',)

class QuestrSocialSignupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)

    class Meta:
        model = QuestrUserProfile
        fields = ['first_name','last_name','displayname','email']
        exclude = ('username.help_text',)


class QuestrUserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given data
    """
    error_messages = {
        'duplicate_username': _("A user with that username already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }
    displayname = forms.RegexField(label=_("Username"), max_length=30,
        regex=r'^[\w.\.+-]+$',
        help_text=_("Required. 30 characters or fewer. Letters, digits and "
                      "./+/-/_ only."),
        error_messages={
            'invalid': _("This value may contain only letters, numbers and "
                         "./+/-/_ characters.")})
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = QuestrUserProfile
        fields = ['first_name','last_name','displayname','email',]
        widget = {
            'first_name' : forms.TextInput(attrs = { 'placeholder': 'First Name'}),
            'last_name' : forms.TextInput(attrs = { 'placeholder': 'Last Name'}),
            'email' : forms.TextInput(attrs = { 'placeholder': 'Email Address: me@example.com'}),
            'displayname' : forms.TextInput(attrs = { 'placeholder': 'displayname: Can contain .,+,- OR _'}),
            'password1' : forms.PasswordInput(attrs = { 'placeholder': 'Password'}),
            'password2' : forms.PasswordInput(attrs = { 'placeholder': 'Confirm Password'}),
        }

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        displayname = self.cleaned_data["displayname"]
        try:
            QuestrUserProfile._default_manager.get(displayname=displayname)
        except QuestrUserProfile.DoesNotExist:
            return displayname
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )

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

    def check_for_test_cookie(self):
        warnings.warn("check_for_test_cookie is deprecated; ensure your login "
                "view is CSRF-protected.", DeprecationWarning)

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache