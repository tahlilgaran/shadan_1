__author__ = 'farzanehtahooni'
# -*- coding: utf-8 -*-​

from django import forms
from time_system.models import UserProfile
from django.contrib.auth.models import User


class UserForm(forms.Form):
        username = forms.CharField( required= False, label='نام کاربری')
        password = forms.CharField(required=False , widget=forms.PasswordInput , label='رمز عبور')

class UserRegisterForm(forms.ModelForm):
    firstname = forms.CharField(required=True , label='نام')
    lastname = forms.CharField(required=True , label='نام خانوادگی')
    username = forms.CharField(required=True, label='نام کاربری')
    password = forms.CharField(required=True , widget=forms.PasswordInput , label='رمز عبور')
    password_again = forms.CharField(required=True , widget=forms.PasswordInput , label='تکرار رمز عبور')

    class Meta:
        model = UserProfile
        fields = ('phoneNumber' , 'image')

    def __init__(self , *args , **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = ['firstname', 'lastname', 'username','password','password_again','phoneNumber','image']

    def clean_username(self):
        username = self.cleaned_data['username']
        if not username:
            raise forms.ValidationError("پر کردن این قسمت الزامی است.")
        if len(username) < 4:
            raise forms.ValidationError("نام کاربری کمتر از ۴ حرف دارد.")
        try:
            user = User.objects.exclude(pk=self.instance.pk).get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('نام کاربری قبلا استفاده شده است.')

    def clean_firstname(self):
        firstname = self.cleaned_data['firstname']
        if not firstname:
            raise forms.ValidationError("پر کردن این قسمت الزامی است.")
        return firstname

    def clean_lastname(self):
        lastname = self.cleaned_data['lastname']
        if not lastname:
            raise forms.ValidationError("پر کردن این قسمت الزامی است.")
        return lastname

    def clean_password(self):
        password = self.cleaned_data['password']
        if not password:
            raise forms.ValidationError("پر کردن این قسمت الزامی است.")
        if len(password) < 4:
            raise forms.ValidationError("رمز عبور باید از ۴ کاراکتر بیشتر باشد.")
        return password

    def clean_password_again(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password_again')

        if not password2:
            raise forms.ValidationError("پر کردن این قسمت الزامی است.")
        if password1 != password2:
            raise forms.ValidationError("رمز عبور مطابقت ندارد.")
        return password2


    def save(self , commit=True):
        user = User.objects.create_user(password=self.cleaned_data['password'] , username=self.cleaned_data['username'])
        profile = super(UserRegisterForm,self).save(commit=False)
        profile.user = user
        user.first_name = self.cleaned_data['firstname']
        user.last_name = self.cleaned_data['lastname']
        user.save()
        profile.save()
        print user.last_name