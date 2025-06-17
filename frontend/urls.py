
from django.urls import path
from .views import home,index
from . import views


urlpatterns = [   
    path("sitemap.xml", views.sitemap, name="sitemap.xml"),

    path('login/', views.frontend_login, name='frontend_login'),
    path('logout/', views.frontend_logout, name='frontend_logout'),
    path('register/', views.frontend_register, name='frontend_register'),



    path('blog/', views.blog_list, name='blog'),
    path('blog/<slug:slug>/', views.post_detail, name='post-detail'),
    path('category/<slug:slug>/', views.category_posts, name='category-posts'),
    path('post/like/', views.like_post, name='like_post'),

    

    path('', home, name='home'),
    path('<str:code>/', index, name='dynamic_page'),
    path('<str:code>/<str:para>/', index, name='dynamic_page_with_param'),
    path('contactus/', views.index,{'code': 'contactus'}, name='contactus'),

    path('send-email-loudoun', views.send_email_loudoun, name='send_email_loudoun'),
	path('send-email-fairfax', views.send_email_fairfax, name='send_email_fairfax'),	
    
]