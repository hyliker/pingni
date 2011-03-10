#coding: utf-8
from django import forms
from django.contrib.auth.models import User
from captcha.fields import CaptchaField
from commentit.models import Comment

class CommentForm(forms.ModelForm):
    captcha = CaptchaField(label=u"验证码", error_messages={"invalid": u"你输入的验证码不正确, 请重新输入"} )
    class Meta:
        model = Comment
        fields = ("content",) 
