from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'city', 'postal_code', 'country']
        widgets = {
            'address': forms.TextInput(attrs={'placeholder': 'Enter your address'}),
            'city': forms.TextInput(attrs={'placeholder': 'Enter your city'}),
            'postal_code': forms.TextInput(attrs={'placeholder': 'Enter postal code'}),
            'country': forms.TextInput(attrs={'placeholder': 'Enter your country'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Enter your phone number'}),
        }