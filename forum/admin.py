from django.contrib import admin

# Register your models here.

from .models import ForumCategory, ForumPost, ForumReply

admin.site.register(ForumCategory)
admin.site.register(ForumPost)
admin.site.register(ForumReply)