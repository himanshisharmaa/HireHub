from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class EmployerSignUpForm(UserCreationForm):
    class Meta:
        model=User
        fields=["username","email","password1","password2"]

    def save(self,commit=True):
        user=super().save(commit)
        user.profile.is_employer=True
        if commit:
            user.save()
            user.profile.save()
        return user

class CandidateSignUpForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']

    def save(self,commit=True):
        user=super().save(commit)
        user.profile.is_employer=False
        if commit:
            user.save()
            user.profile.save()
        return user

from django import forms
from .models import Profile

class CandidateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'bio', 'location', 'skills', 'resume']

class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'bio', 'location']
