

from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Review



class ReviewForm(forms.ModelForm):
    """
    A form that creates a post, from the given data
    """
    class Meta:
        model = Review
        exclude = ['quest','reviewed','final_rating', 'rating_1', 'rating_2', 'rating_3', 'rating_4']