from django import forms

from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta():
        model = UserProfile
        fields = ['name', 'bio', 'profile_img', 'intrest']