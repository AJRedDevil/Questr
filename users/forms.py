from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import QuestrUserProfile

class QuestrUserChangeForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        for fieldname in ['username']:
            self.fields[fieldname].help_text = None
            del self.fields['password']

            #changed label for form items
        self.fields['privacytoggle'].label = "Privacy"
        self.fields['biography'].label = "Your biography"

    class Meta:
        model = QuestrUserProfile
        fields = ['first_name','last_name','username','email','phone','biography','privacytoggle']
        exclude = ('username.help_text',)


class QuestrUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.fields['password1'].required = True
        self.fields['password2'].required = True
        self.fields['username'].required = True

    class Meta:
        model = QuestrUserProfile
        fields = ['first_name','last_name','username','email','password1','password2']

    def check_password_match(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            msg = "Passwords don't match"
            raise forms.ValidationError("Password mismatch")
        return password2

    def save(self, commit=True):
        user = super(QuestrUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password2"])
        if commit:
            user.save()
        return user