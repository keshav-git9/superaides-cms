from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from backend.models import Contactus,Comment
from django.contrib.auth import authenticate
from captcha.fields import CaptchaField

class ContactusForm(forms.ModelForm): 
    captcha = CaptchaField()    
    class Meta:
        model = Contactus
        fields = '__all__'       

class CommentForm(forms.ModelForm):
    captcha = CaptchaField() 
    class Meta:
        model = Comment        
        fields = ['name', 'email', 'content']

