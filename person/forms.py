#coding: utf-8
from django import forms
from person.models import Profile
from django.contrib.auth.models import User
from captcha.fields import CaptchaField

class ProfileForm(forms.ModelForm):
    email = forms.EmailField(label=u"电子邮箱",  required=True)
    class Meta:
        model = Profile
        fields = ("nickname", "email", "avatar", "sign", "location", "website", "is_noticed")

class RegisterForm(forms.ModelForm):
    captcha = CaptchaField(label=u"验证码", error_messages={"invalid": u"你输入的验证码不正确, 请重新输入"} )
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields["password"].widget = forms.PasswordInput()
        self.fields["email"].required = True
    class Meta:
        model = User
        fields = ("username", "email", "password")

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
