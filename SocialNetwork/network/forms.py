__author__ = 'farzanehtahooni'

from django import forms
from users.models import Profile,User

class UserProfileForm(forms.ModelForm):

    first_name = forms.CharField(required=True , max_length=250)
    last_name  = forms.CharField(required=False ,max_length=250)

    class Meta:
        model = Profile
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        profile = super(UserProfileForm,self).save(commit=False)
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        profile.user.first_name = first_name
        profile.user.last_name = last_name
        profile.user.save()
        profile.save()

