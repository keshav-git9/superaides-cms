from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from backend.models import Contactus,Comment
from django.contrib.auth import authenticate

class ContactusForm(forms.ModelForm):    
    class Meta:
        model = Contactus
        fields = '__all__'       

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'content']