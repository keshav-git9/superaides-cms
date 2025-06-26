from django.urls import path 
from django.contrib.auth import views as auth_views
from . import views



urlpatterns = [
    path('register/',views.register_view,name='register'),
    path('login/',views.login_view,name='login'),
    path('forgot_password/',views.forgot_password_view,name='forgot_password'),
    path('logout/',views.logout_view,name='logout'),
    path('dashboard/',views.dashboard_view,name='dashboard'),

    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='auth/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='auth/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete.html'), name='password_reset_complete'),

	path('add-html/',views.addhtml_view,name='add-html'),	
    path('list-html/', views.listHtml_view, name = 'list-html'),
    path('edit-html/<int:id>/', views.edithtml_view, name='edit-html'),
    path('html-status/', views.change_html_status, name='change_html_status'),
    path('delete-html/', views.delete_html, name='delete-html'),
    
    path('page-list/', views.pagelist, name = 'page-list'),
    path('page-add/',views.page_add,name='page-add'),
    path('page-edit/<int:id>/', views.page_edit, name='page-edit'),   
    path('find-page-title/', views.find_page_title, name = 'find-page-title'),
    path('page-status/', views.change_page_status, name='change_page_status'),
    path('delete-page/', views.delete_page, name='delete-page'),


    path('navi-group/', views.navigroup, name = 'navi-group'),
    path('navi-group-add/',views.navigroup_add,name='navi-group-add'),
    path('navi-group-edit/<int:id>/', views.navigroups_edit, name='navi-group-edit'),
    path('navig-status/', views.change_navig_status, name='change_navig_status'),

    path('navi-group-page/<int:nid>/', views.navigrouppage, name = 'navi-group-page'),
    path('navi-group-page-add/<int:nid>/',views.navigrouppage_add,name='navi-group-page-add'),    
    path('navi-group-page-edit/<int:nid>/<int:id>/', views.navigroupspage_edit, name='navi-group-page-edit'),
    path('navigpage-status/', views.change_navigpage_status, name='change_navigpage_status'),
    path('delete-navigpage/', views.delete_navigpage, name='delete-navigpage'),


    path('navi-group-child-page/<int:npid>/', views.navigroupchildpage, name = 'navi-group-child-page'),
    path('navi-group-child-page-add/<int:npid>/',views.navigroupchildpage_add,name='navi-group-child-page-add'),    
    path('navi-group-child-page-edit/<int:npid>/<int:id>/', views.navigroupschildpage_edit, name='navi-group-child-page-edit'),

    path('contact-us/', views.contactus, name = 'contact-us'),

    path('contact-delete/', views.delete_all_contact, name = 'contact-delete'),
    path('send-email/', views.send_email, name='send_email'),

    path('setting/',views.setting_view, name='setting'),
    path('add_logo/',views.add_logo, name='add_logo'),			


    path('post-list/', views.post_list, name='post-list'),
    path('post-add/',views.post_add,name='post-add'),
    path('post-edit/<int:id>/', views.post_edit, name='post-edit'), 
    path('post-status/', views.change_post_status, name='change_post_status'),
    path('delete-post/', views.delete_post, name='delete-post'),
    
    path('comment-list/', views.comment_list, name='comment-list'),
    path('comment-list/<int:cpid>/', views.comment_list, name='comment-list'),		
	path('comment-status/', views.comment_status, name='comment-status'),			
    path('delete-comment/', views.delete_comment, name='delete-comment'),


    path('category-list/', views.category, name='category-list'),
    path('category-add/',views.category_add,name='category-add'),
    path('category-edit/<int:id>/', views.category_edit, name='category-edit'), 


    path('testimonials-list/', views.testimonials_list, name='testimonials-list'),
	path('testimonials-add/',views.testimonials_add,name='testimonials-add'),		
	path('testimonials-edit/<int:id>/', views.testimonials_edit, name='testimonials-edit'), 
	path('testimonials-status/', views.testimonials_status, name='testimonials-status'),
	path('delete-testimonials/', views.delete_testimonials, name='delete-testimonials'),	


    path('post-tag_list/', views.tag_list, name = 'post-tag-list'),
    path('post-tag-add/',views.post_tag_add,name='post-tag-add'),
    path('post-tag-edit/<int:id>/', views.post_tag_edit, name='post-tag-edit'),

    #path('postcommentlist/<slug:slug>/', views.post_comment, name='postcomment-list'),
    #path('change-status/', views.change_comment_status, name='change_comment_status'),


    path('groups/', views.group_list, name='group-list'),
    path('groups/add/', views.group_add, name='group-add'),
    path('group-edit/<int:id>/', views.group_edit, name='group-edit'),
    path('group-delete/', views.group_delete, name='group-delete'),


    path('users-list/', views.users, name='users-list'),
    path('users-add/', views.users_add, name='users-add'),
    path('users-edit/<int:id>/', views.users_edit, name='users-edit'),
    path('users-status/', views.users_status, name='users-status'),
    path('users-delete/', views.users_delete, name='users-delete'),














    path('seo-analysis/', views.seo_view, name='seo_analysis'),
]