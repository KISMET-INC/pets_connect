from django.urls import path
from . import views
from django.contrib import admin 
from django.urls import path 
from django.conf import settings 
from django.conf.urls.static import static 
from .views import *


urlpatterns = [

    path('', views.landing),
    path('register', views.register),
    path('signin', views.signin),
    path('process_register', views.process_register),
    path('process_signin', views.process_signin),
    path('logout', views.logout),
    path('welcome_testers', views.welcome_testers),
    
    # Views
    path('bulletin/<int:user_id>/<int:image_id>/<int:modal_trigger>', views.bulletin),
    path('explore', views.explore),
    path('edit_user/<int:user_id>', views.edit_user),
    path('profile/<int:user_id>', views.profile),
    
    # Image Proceses
    path('process_add_pet_image', views.process_add_pet_image),
    path('process_remove_image/<int:image_id>', views.process_remove_image),
    
    # User Proceses
    path('process_edit_user', views.process_edit_user),
    path('process_remove_user/<int:user_id>', views.process_remove_user),
    
    # Comment Processes
    path('process_delete_comment/<int:comment_id>/<str:component>',views.process_delete_comment),
    path('process_add_comment', views.process_add_comment),
    
    # Stat Processes
    path('process_heart/<int:image_id>/<str:location>', views.process_heart),
    path('process_follow/<int:user_to_follow_id>/<image_id>', views.process_follow),
    
    # Ajax - replace HTML
    path('replace_stats/<int:image_id>', views.replace_stats),
    path('replace_comments/<int:image_id>', views.replace_comments),
    path('replace_post/<int:image_id>', views.replace_post),
    path('replace_modal/<int:image_id>', views.replace_modal),
    path('replace_image/<int:image_id>', views.replace_image),

    # Ajax  -get info from database
    path('get_session_id', views.get_session_id),
    path('get_image_list/<int:user_id>', views.get_image_list),
    path('get_heart_sum/<int:image_id>', views.get_heart_sum),
    path('get_more_images', views.get_more_images),
    # Admin
    path('explore/admin', views.admin),
    path('admin_edit_user/<int:user_id>/<int:image_id>/<int:modal_trigger>', views.admin_edit_user),
    
   # path('process_admin_edit_user/<int:user_id>', views.process_admin_edit_user),

    # not using yet
    path('process_edit_password', views.process_edit_password),

]