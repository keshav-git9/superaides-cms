from django.urls import path
from . import views

urlpatterns = [
    path('', views.forum_home, name='forum_home'),
    path('category/<int:id>/', views.forum_category, name='forum_category'),
    path('post/<int:id>/', views.forum_post_detail, name='forum_post_detail'),
    path('post/create/', views.forum_post_create, name='forum_post_create'),
]
