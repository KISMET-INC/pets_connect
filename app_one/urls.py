from django.urls import path
from . import views
from django.contrib import admin 
from django.urls import path 
from django.conf import settings 
from django.conf.urls.static import static 
from .views import *


urlpatterns = [

    # path('',views.landing),
    path('main_page', views.main_page),
    path('logout', views.logout),
    path('read_all',views.read_all),
    path('process_register', views.process_register),
    path('process_signin', views.process_signin),
    path('process_remove_user/<int:user_id>', views.process_remove_user),

    path('', views.home),
    path('signin', views.signin),
    path('register', views.register),
    path('dashboard/admin', views.admin),
    path('users/new', views.new),
    path('users/add_image/<int:user_id>', views.add_image),
    path('users/edit_user/<int:user_id>', views.edit_user),
    path('users/remove_user/<int:user_id>', views.process_remove_user),
    path('dashboard/<int:image_id>', views.dashboard),
    path('users/edit_self', views.edit_self),
    

    path('process_edit_password', views.process_edit_password),
    path('process_edit_user', views.process_edit_user),
    path('process_edit_self', views.process_edit_self),
    path('process_add_image', views.process_add_image),
    path('process_remove_image/<int:image_id>', views.process_remove_image),
    path('process_add_comment', views.process_add_comment),
    path('process_like/<int:image_id>', views.process_like),
    

]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)