from django import forms
from .models import CustomUser



class EditProfileForm(forms.ModelForm):
    
    class Meta:
        model = CustomUser
        fields = ['full_name', 'avatar', 'birthday', 'email', 'phone_number', 'bio', 'gender']