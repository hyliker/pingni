#coding: utf-8
from django import forms
from show.models import Show
from captcha.fields import CaptchaField

class ShowForm(forms.ModelForm):
    def clean(self):
        cleaned_data = self.cleaned_data
        image = cleaned_data.get("image")
        image_url = cleaned_data.get("image_url")
        if not image_url and not image:
            raise forms.ValidationError(u"上传照片")
        return cleaned_data

    class Meta:
        model = Show
        exclude = ("user", "read_count", "like_count", "comment_count", "likes" )
