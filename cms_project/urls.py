"""
URL configuration for cms_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import handler404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required



urlpatterns = [
    path('admin/', admin.site.urls),
    path('superaides-cms/',include('backend.urls')),
    #path('auth/',include('backend.urls')),
    
    path('forum/', include('forum.urls')),  

	path('ckeditor/', include('ckeditor_uploader.urls')),
	path('', include('frontend.urls')),  	
    path('captcha/', include('captcha.urls')),		
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



@login_required
def custom_404_view(request, exception):
    return render(request, '404.html', status=404)
# Tell Django to use this function for 404 errors
handler404 = custom_404_view

handler404 = 'frontend.views.custom_404'