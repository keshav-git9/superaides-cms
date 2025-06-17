from django.contrib import admin
from .models import (CustomUser,Html,Cms_setting,Pages,Navigroups,Navigroupspages,Contactus,Post,Tag,Category,Comment,Testimonial)

# Register your models here.
admin.site.register(CustomUser)

#admin.site.register(Html)
@admin.register(Html)
class HtmlAdmin(admin.ModelAdmin):
    # Display all fields in the list view
   # list_display = ['code', 'title', 'description', 'contents']
    #list_display = [field.name for field in Html._meta.fields]
    list_display = (
        "code",
        "title",
        "description",
        "contents"        
    	)
    search_fields = (
        "code",
        "title"       
    )
    #search_fields = ['code', 'title']  # Enable search for specific fields
   # list_filter = ['code', 'title']
    list_per_page = 20   



@admin.register(Pages)
class PagesAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "code",       
        "status"              
    	)
    search_fields = (
        "code",
        "title"       
    )   
    list_per_page = 20  


@admin.register(Navigroups)
class NavigroupsAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "code", 
    	)
    search_fields = (
        "code",
        "title"       
    )   
    list_per_page = 20  

@admin.register(Navigroupspages)
class NavigroupspagesAdmin(admin.ModelAdmin):
    list_display = (   
        "id",     
        "navi_code",        
        "parent",
        "page",
        "external_link",
    	)
    search_fields = (  
        "id",       
        "navi_code",       
        "parent",
        "page",
        "external_link",     
    )   
    list_per_page = 20       

@admin.register(Contactus)
class ContactusAdmin(admin.ModelAdmin):
    # Display all fields in the list view  
    list_display = (
        "fullname", "email", "phone",                   
    	)
    search_fields = (
        "fullname", "email", "phone",         
    )   
    list_per_page = 20   
 			


@admin.register(Cms_setting)
class Cms_settingAdmin(admin.ModelAdmin):
    # Display all fields in the list view  
    list_display = (
        "existing_logo_title",               
    	)
    search_fields = (
        "existing_logo_title",         
    )   
    list_per_page = 20   


admin.site.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Display all fields in the list view  
    list_display = (
        "title","slug","category"               
    	)
    search_fields = (
        "title",         
    )   
    list_per_page = 20   

admin.site.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Display all fields in the list view  
    list_display = (
        "name","slug"               
    	)
    search_fields = (
        "name",         
    )   
    list_per_page = 20   

admin.site.register(Tag)

admin.site.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'created_at', 'is_approved')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'rating')
    search_fields = ('name', 'message')