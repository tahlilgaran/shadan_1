from django import forms
from .models import Profile
from django.contrib.auth.models import User


class SignUpForm(forms.ModelForm):
    firstname = forms.CharField(required=True)
    lastname = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)
    confirm_password = forms.CharField(required=True)

    class Meta:
        model = Profile
        fields = ('location','birthday')

    def __init__(self , *args , **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget = forms.EmailInput(attrs={
            'class': 'form-control','placeholder': 'Enter email'})
        self.fields['firstname'].widget = forms.TextInput(attrs={
            'class': 'form-control','placeholder': 'Enter your first name'})
        self.fields['lastname'].widget = forms.TextInput(attrs={
            'class': 'form-control','placeholder': 'Enter your last name'})
        self.fields['username'].widget = forms.TextInput(attrs={
            'class': 'form-control','placeholder': 'choose a username'})
        self.fields['password'].widget = forms.PasswordInput(attrs={
            'class': 'form-control','placeholder': 'at least 6 character'})
        self.fields['confirm_password'].widget = forms.PasswordInput(attrs={
            'class': 'form-control','placeholder': 'repeat your password'})
        self.fields['birthday'].widget = forms.DateInput(attrs={
            'class': 'form-control','placeholder': 'yyyy-mm-dd'})
        self.fields['location'].widget = forms.TextInput(attrs={
            'class': 'form-control','placeholder': 'your city or country'})
        self.fields.keyOrder = ['email', 'username','firstname', 'lastname','password','confirm_password', 'birthday', 'location']

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.exclude(pk=self.instance.pk).get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("this username has assigned before")

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 6:
            raise forms.ValidationError("your password's length must be more than 6 character")
        return password

    def clean_confirm_password(self):

        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('confirm_password')
        if password1 != password2:
            raise forms.ValidationError(" the passwords doesn't match")
        return password2

    def save(self, commit=True):
        user = User.objects.create_user(password=self.cleaned_data['password'], username=self.cleaned_data['username']
                                        ,email=self.cleaned_data['email'])
        profile = super(SignUpForm,self).save(commit=False)
        profile.user = user
        profile.user.first_name = self.cleaned_data['firstname']
        profile.user.last_name = self.cleaned_data['lastname']
        profile.user.save()
        profile.birthday = self.cleaned_data['birthday']
        if self.cleaned_data['location'] :
            profile.location = self.cleaned_data['location']
        profile.save()