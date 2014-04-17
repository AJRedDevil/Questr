from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import QuestrUserProfile

class QuestrUserProfileForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        for fieldname in ['username']:
            self.fields[fieldname].help_text = None
            del self.fields['password']

            #changed label for form items
        self.fields['privacyToggle'].label = "Privacy"
        self.fields['biography'].label = "Your biography"

    class Meta:
        model = QuestrUserProfile
        fields = ['first_name','last_name','username','email','phone','biography','privacyToggle']
        exclude = ('username.help_text',)


