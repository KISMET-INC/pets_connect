from django.urls import path
from . import views


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
    path('users/show/<int:user_id>', views.show),
    path('users/edit_user/<int:user_id>', views.edit_user),
    path('users/remove_user/<int:user_id>', views.process_remove_user),
    path('dashboard', views.dashboard),
    path('users/edit_self', views.edit_self),
    

    path('process_edit_password', views.process_edit_password),
    path('process_edit_user', views.process_edit_user),
    path('process_edit_self', views.process_edit_self),
    path('process_add_message', views.process_add_message),
    path('process_add_comment', views.process_add_comment),
    

]
