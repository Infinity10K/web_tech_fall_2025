from django import forms
from django.contrib.auth.models import User

from app.models import Profile, Question


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label="Username")
    password = forms.CharField(widget=forms.PasswordInput)

    # def clean_username(self):
    #     username = self.cleaned_data['username']
    #     if username != 'admin':
    #         raise forms.ValidationError('Please enter a valid username.')
    #     return username

    # def clean(self):
    #     cleaned_data = super().clean()
    #     if cleaned_data.get('username') == 'admin':
    #         raise forms.ValidationError('Please enter a valid username!!!!.')
    #     return cleaned_data


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100, label="Username")
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    email = forms.EmailField(max_length=100, label="Email")
    avatar = forms.ImageField(label="Avatar", required=False)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cleaned_data

    def save(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        email = self.cleaned_data['email']

        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        Profile.objects.create(user=user, avatar=self.cleaned_data['avatar'])
        return user


