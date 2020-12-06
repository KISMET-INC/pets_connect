from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt


#=============================================##
# read_all()
# RENDERS table to see all users in database
# with the ability to delete users
#=============================================##
def read_all(request):
    context = {
        'users': User.objects.all()
    }
    return render(request,'example_templates/read_all.html',context)


#=============================================##
# process_remove_user()
# PROCESSES the deletion of a user in the
# database.  REDIRECTS to read_all table
#=============================================##
def process_remove_user(request, user_id):
    this_user = User.objects.get(id = user_id)
    this_user.delete()
    return redirect('/dashboard')


#=============================================##
# process_register()
# return redirect('/')
#=============================================##
def process_register(request):
    post = request.POST
    errors = User.objects.basic_validator(post)
    
    
    if len(errors) > 0:
        for value in errors.values():
            messages.error(request,value)
        return redirect('/register')
    
    else :
        hash = bcrypt.hashpw(post['pass'].encode(), bcrypt.gensalt()).decode()
        user_level = 0

        users = User.objects.all()
        if len(users) < 1:
            user_level = 9

        
        new_user = User.objects.create(first_name=post['first'], last_name=post['last'], password = hash, email = post['email'], user_level= user_level)

        if new_user.user_level == 9:
            return redirect('/dashboard/admin')

        if user_level not in request.session:
            request.session['user_id'] = new_user.id
            request.session['user_name'] = new_user.first_name
            request.session['user_level'] = new_user.user_level
            return redirect('/dashboard')

        return redirect('/dashboard')




#=============================================##
# logout()
# Deletes the session keys and 
# REDIRECTS to root
#=============================================##
def logout(request):
    request.session.flush()
    return redirect('/')

#=============================================##
# process_signin()
# PROCESSES process_signin request
# REDIRECTS back to root with errors or
# to process_signin page on success
#=============================================##
def process_signin(request):
    post = request.POST
    user = User.objects.filter(email = post['email'])
    errors = User.objects.basic_validator_login(post)
    print(errors)

    if len(errors) > 0:
        for value in errors.values():
            messages.error(request,value)
        return redirect('/signin')
    
    else:
            this_user = User.objects.get(id = user[0].id)
            request.session['user_id'] = this_user.id
            request.session['user_name'] = this_user.first_name
            request.session['user_level'] = this_user.user_level
            if this_user.user_level == 9:
                return redirect('/dashboard/admin')
            return redirect('/dashboard')


#=============================================##
# landing()
# RENDERS login_reg.html
#=============================================##
def landing(request):
    users = User.objects.all()
    return render(request,'example_templates/login_reg.html')

#=============================================##
# END LOGIN DEFS
#=============================================##

#=============================================##
# START PAGE DEFS
#=============================================##


#=============================================##
# main_page()
# RENDERS books login html if User_iD
# session key is avaiable
# WITHOUT KEY REDIRECTS to root
#=============================================##
def main_page(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        return render(request,'landing.html')





#=============================================##
# home()
#
#=============================================##
def home(request):
    return render(request,'home.html')

#=============================================##
# signin()
#
#=============================================##
def signin(request):
    return render(request,'signin.html')

#=============================================##
# register()
#
#=============================================##
def register(request):
    return render(request,'register.html')

#=============================================##
# admin()
#
#=============================================##
def admin(request):
    context = {
        'users': User.objects.all()
    }
    return render(request,'admin.html',context)

#=============================================##
# new()
#
#=============================================##
def new(request):   
    return render(request,'new.html')

#=============================================##
# show()
#
#=============================================##
def show(request, user_id):
    context = {
        'user': User.objects.get(id=user_id),
        'user_messages': Message.objects.filter(user_to_id = user_id).order_by("-created_at"),
    }
    return render(request,'show.html',context)

#=============================================##
# edit_user()
#
#=============================================##
def edit_user(request,user_id):
    context = {
        'current_user' : User.objects.get(id=request.session['user_id']),
        'user': User.objects.get(id=user_id)
    }
    return render(request,'edit_user.html',context)

#=============================================##
# dashboard()
#
#=============================================##
def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/signin')
    else:
        context = {
            'current_user': User.objects.get(id=request.session['user_id']),
            'users' : User.objects.all()
        }

        if request.session['user_level'] == 0:
            return render(request,'dashboard.html',context)
    return render(request,'admin.html',context)

#=============================================##
# edit_self()
#
#=============================================##
def edit_self(request):
    context = {
            'current_user': User.objects.get(id=request.session['user_id']),
    }
    return render(request,'edit_self.html',context)


#=============================================##
# remove_user()
#
#=============================================##
def remove_user(request,user_id):
    return render(request,'dashboard.html')


#=============================================##
# process_edit_password()
# return redirect('/')
#=============================================##
def process_edit_password(request):
    errors = User.objects.basic_validator_passwords(request.POST)
    print(request.POST['user_id'])
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/users/edit_user/{request.POST["user_id"]}')
    else:
        user = User.objects.get(id=request.POST['user_id'])
        user.password = request.POST['pass']

        
    return redirect(f'/users/show/{user.id}')

#=============================================##
# process_edit_user()
# return redirect('/')
#=============================================##
def process_edit_user(request):
    user = User.objects.get(id=request.POST['user_id'])
    post = request.POST
    errors = User.objects.basic_validator_edit_user(post)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/users/edit_user/{user.id}')
    else:
        
        user.email = request.POST['email']
        user.first_name = request.POST['first']
        user.last_name = request.POST['last']
        user.save()

        return redirect(f'/dashboard')

#=============================================##
# process_edit_self()
# return redirect('/')
#=============================================##
def process_edit_self(request):
    return render(request,'process_edit_self.html')

#=============================================##
# process_add_message()
# return redirect('/')
#=============================================##
def process_add_message(request):
    post = request.POST
    print(request.POST)

    current_user = User.objects.get(id=request.session['user_id'])
    user_to_message = User.objects.get(id=post['user_id'])
    this_message = Message.objects.create(text = post['text'], user_to = user_to_message, user_from = current_user )
    user_messages = Message.objects.filter(user_to_id = 1)

    print(user_messages)
    return redirect (f'/users/show/{user_to_message.id}')

#=============================================##
# process_add_comment()
# return redirect('/')
#=============================================##
def process_add_comment(request):
    post = request.POST
    print(request.POST)

    this_message = Message.objects.get(id = post['message_id'])
    new_comment = Comment.objects.create(text = post['text'], message = this_message)


    return redirect (f'/users/show/{this_message.user_to.id}')
