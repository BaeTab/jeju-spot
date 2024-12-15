from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    bio = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}), 
        required=False
    )
    profile_image = forms.ImageField(
        widget=forms.FileInput, 
        required=False
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'bio', 'profile_image')

class CustomUserChangeForm(UserChangeForm):
    email = forms.EmailField(required=True)
    bio = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}), 
        required=False
    )
    profile_image = forms.ImageField(
        widget=forms.FileInput, 
        required=False
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'bio', 'profile_image')

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['bio', 'profile_image']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
        }
