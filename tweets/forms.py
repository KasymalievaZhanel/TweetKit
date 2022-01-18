from dataclasses import field
from unittest.util import _MAX_LENGTH
from django import forms
from django.conf import settings

from .models import Tweet

MAX_TWEET_LENGTH = settings.MAX_LENGTH

class TweetForm(forms.ModelForm):
    #content = forms.CharField
    class Meta:
        model = Tweet
        fields = ['content']

    def clean_content(self):
        content = self.cleaned_data.get("content")
        if len(content) > MAX_LENGTH:
            raise forms.ValidationError("This tweet is too long")
        if len(content) == 0:
            raise forms.ValidationError("This tweet is too small") 
        return content    