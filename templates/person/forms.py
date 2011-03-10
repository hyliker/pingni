#coding: utf-8
from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(required=True, label=u"用户名")
    email = forms.EmailField(required=True, label=u"邮箱")
    password = forms.CharField(required=True, label=u"密码")
