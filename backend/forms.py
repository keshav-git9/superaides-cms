from django import forms
from ckeditor.widgets import CKEditorWidget
from django.contrib.auth import password_validation
from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ValidationError
from .models import CustomUser,Html,Cms_setting,Pages,Navigroups,Navigroupspages,Post,Category,Comment,Tag,Testimonial
from django.contrib.auth import authenticate


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.SelectMultiple,
        required=True
    )
    
    class Meta:
        model = CustomUser
        fields = ["name", "email", "mobile", "password","confirm_password", 'groups' ]
        widgets = {'password': forms.PasswordInput()}

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError({"password": "Password fields didn't match."})

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data["password"]
        user.set_password(password)
        if commit:
            user.save()
        return user

class UserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'mobile', 'is_active', 'groups']  # Add any other fields you want editable

    




class LoginForm(forms.Form):
    username = forms.CharField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        print("USER NAME",username)

        if username and password:
            self.user = authenticate(username=username, password=password)
            print("USER",self.user)
            if not self.user:
                raise forms.ValidationError("Invalid login credentials. Please try again.")

    def get_user(self):
        return self.user if self.is_valid() else None
    

class HtmlForm(forms.ModelForm):
    contents = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Html
        fields = '__all__'
        #fields = ['code', 'title', 'description', 'contents']



class PageForm(forms.ModelForm):
    contents = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Pages
        fields = '__all__'       

class NavigroupForm(forms.ModelForm):    
    class Meta:
        model = Navigroups
        fields = '__all__'

class NavigrouppageForm(forms.ModelForm):    
    class Meta:
        model = Navigroupspages
        fields = '__all__'
       

class logoandfavicon(forms.ModelForm):
    class Meta:
        model = Cms_setting
        fields = ['existing_logo_title', 'existing_logo', 'footer_logo', 'existing_favicon']  # Update personal info fields

class socialmediapages(forms.ModelForm):
    class Meta:
        model = Cms_setting
        fields = ['facebook_link','instagram_link','twitter_link','youtube_link']  # Update only the description


class googlerecaptcha(forms.ModelForm):
    class Meta:
        model = Cms_setting
        fields = ['recapcha_allow','site_key','secret_key']  # Update only the status 

class googleanalytic(forms.ModelForm):
    class Meta:
        model = Cms_setting
        fields = ['analytic_allow','analytic_id']  # Update only the status 

class sociallogin(forms.ModelForm):
    class Meta:
        model = Cms_setting
        fields = ['social_allow','gmail_client_id','gmail_secret_id','gmail_redirect_url']  # Update only the status 

class facebookpixel(forms.ModelForm):
    class Meta:
        model = Cms_setting
        fields = ['fpixel_allow','fapp_id']  # Update only the status 

class PostForm(forms.ModelForm):
    contents = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Post
        fields = '__all__'    
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

class CategoryForm(forms.ModelForm):    
    class Meta:
        model = Category
        fields = '__all__'   

class TagForm(forms.ModelForm):    
    class Meta:
        model = Tag
        fields = '__all__'

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'content']


class GroupForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Permissions"
    )
    class Meta:
        model = Group
        fields = ['name', 'permissions']

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['name', 'designation', 'contents', 'rating', 'photo']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f'{i} Star{"s" if i > 1 else ""}') for i in range(1, 6)])
        }