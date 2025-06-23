from django.urls import reverse
from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,Group
from django.utils import timezone
from django.utils.text import slugify
from .managers import CustomUserManager
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Create your models here.

class CustomUser(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=10, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.name
    
    def has_module_perms(self, app_label):
        # Assuming all users have permission to access all modules
        return True
    
    def has_perm(self, perm, obj=None):
        # For simplicity, assuming all users have all permissions
        return True


class Html(models.Model):
    code = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    description = models.TextField()
    contents = RichTextUploadingField()
    status = models.IntegerField(default=0,blank=True, null=True)

    def __str__(self):
        return self.code
    def get_absolute_url(self):
        return f'/html/{self.id}/'

class Pages(models.Model):
    title = models.CharField(max_length=200)
    code = models.CharField(max_length=100)
    url = models.CharField(max_length=200, unique=True)
    status = models.IntegerField(default=0)
    contents = RichTextField()
    page_header_image = models.ImageField(upload_to='images/', blank=True, null=True)
    meta_title = models.CharField(max_length=200,blank=True, null=True)
    meta_keyword = models.TextField(blank=True, null=True)
    meta_desc = models.TextField(blank=True, null=True) 
    css = models.TextField(blank=True, null=True)
    js = models.TextField(blank=True, null=True)
    #class Meta:
    #    verbose_name = "Html"
    #    verbose_name_plural = "Htmls"
    def __str__(self):
        return self.title

class Navigroups(models.Model):
    code = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=200)     
    status = models.IntegerField(default=0,blank=True, null=True)
    def __str__(self):
        return self.code

class Navigroupspages(models.Model):
    title = models.CharField(max_length=200,null=True, blank=True)    
    navi_code = models.ForeignKey(Navigroups, on_delete=models.CASCADE, related_name="pages")  # Group link
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name="children")  # Self-referencing for submenus
    page_id = models.IntegerField(default=0,null=True, blank=True)
    page = models.CharField(max_length=100, null=True, blank=True)
    order=models.IntegerField(default=0,null=True, blank=True)
    target=models.IntegerField(default=0,null=True, blank=True)
    external_link=models.CharField(max_length=200,null=True, blank=True) 
    link_type=models.IntegerField(default=0,null=True, blank=True)
    start_image=models.FileField(upload_to='images/', default='images/default_logo.png')
    end_image=models.FileField(upload_to='images/', default='images/default_logo.png')   
    status = models.IntegerField(default=0,null=True, blank=True)
    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class Contactus(models.Model):
    fullname = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=200) 
    phone = models.CharField(max_length=200) 
    subject = models.CharField(max_length=200) 
    message = models.TextField(blank=True, null=True)   
    def __str__(self):
        return self.fullname



class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    cat_status = models.IntegerField(default=1)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    contents = RichTextField()
    post_image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    post_header_image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    meta_title = models.CharField(max_length=200,blank=True, null=True)
    meta_keyword = models.TextField(blank=True, null=True)
    meta_desc = models.TextField(blank=True, null=True) 
    published_at = models.DateTimeField(auto_now_add=True)    
    status = models.IntegerField(default=1,blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts')
    likes = models.PositiveIntegerField(default=0,blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts',null=True,blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()
    status = models.IntegerField(default=0,blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_approved = models.BooleanField(default=True)  # Optional moderation
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"Comment by {self.name} on {self.post.title}"


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100, blank=True)
    contents = models.TextField()
    rating = models.IntegerField(default=5)  # 1 to 5 stars
    photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.rating} Stars"
    

#===============================================================================================
    
class Cms_setting(models.Model):
    existing_logo_title =models.CharField(max_length=250, null=True, blank=True)
    existing_logo = models.FileField(upload_to='images/', default='images/default_logo.png')     
    footer_logo = models.FileField(upload_to='images/', default='images/default_logo.png')
    existing_favicon = models.FileField(upload_to='images/', default='images/default_logo.png')  
    facebook_link = models.CharField(max_length=250, null=True, blank=True)
    instagram_link = models.CharField(max_length=250, null=True, blank=True)
    twitter_link = models.CharField(max_length=250, null=True, blank=True)
    youtube_link = models.CharField(max_length=250, null=True, blank=True)

    recapcha_allow = models.IntegerField(default=0)
    site_key = models.CharField(max_length=250, null=True, blank=True)
    secret_key = models.CharField(max_length=250, null=True, blank=True)

    analytic_allow = models.IntegerField(default=0)
    analytic_id = models.CharField(max_length=250, null=True, blank=True)

    social_allow = models.IntegerField(default=0)
    gmail_client_id = models.CharField(max_length=250, null=True, blank=True)
    gmail_secret_id = models.CharField(max_length=250, null=True, blank=True)
    gmail_redirect_url = models.CharField(max_length=250, null=True, blank=True)

    fpixel_allow = models.IntegerField(default=0)
    fapp_id = models.CharField(max_length=250, null=True, blank=True)

    status = models.IntegerField(default=1)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
            verbose_name = "Cms_setting"
            verbose_name_plural = "Cms_settings"
        
    def __str__(self):
        return self.existing_logo_title or "Unnamed Object"       

"""class Cms_setting(models.Model):
    existing_logo_title =models.CharField(max_length=250)
    existing_logo = models.FileField(upload_to='images/', default='images/default_logo.png')     
    footer_logo = models.FileField(upload_to='images/', default='images/default_logo.png')
    existing_favicon = models.FileField(upload_to='images/', default='images/default_logo.png')  
    facebook_link = models.CharField(max_length=250)
    instagram_link = models.CharField(max_length=250)
    twitter_link = models.CharField(max_length=250)
    youtube_link = models.CharField(max_length=250)

    recapcha_allow = models.IntegerField(default=0)
    site_key = models.CharField(max_length=250)
    secret_key = models.CharField(max_length=250)

    analytic_allow = models.IntegerField(default=0)
    analytic_id = models.CharField(max_length=250)

    social_allow = models.IntegerField(default=0)
    gmail_client_id = models.CharField(max_length=250)
    gmail_secret_id = models.CharField(max_length=250)
    gmail_redirect_url = models.CharField(max_length=250)

    fpixel_allow = models.IntegerField(default=0)
    fapp_id = models.CharField(max_length=250)

    status = models.IntegerField(default=1)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
            verbose_name = "Cms_setting"
            verbose_name_plural = "Cms_settings"
        
    def __str__(self):
        return self.existing_logo_title or 'Unnamed Object'"""
    
#=========================================================================================