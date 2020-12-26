from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt
from .forms import *

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
    return redirect('/dashboard/0')


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

        
        new_user = User.objects.create(user_name=post['first'], password = hash, email = post['email'], user_level= user_level)

        if new_user.user_level == 9:
            return redirect('/dashboard/admin')

        if user_level not in request.session:
            request.session['user_id'] = new_user.id
            request.session['user_name'] = new_user.user_name
            request.session['user_level'] = new_user.user_level
            return redirect('/dashboard/0')

        return redirect('/dashboard/0')




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
            request.session['user_name'] = this_user.user_name
            request.session['user_level'] = this_user.user_level
            if this_user.user_level == 9:
                return redirect('/dashboard/admin')
            return redirect('/dashboard/0')


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
def add_image(request, user_id):
    context = {

        'upload_pet_form': UploadPetForm(),
        'user': User.objects.get(id=user_id),
        'images': Image.objects.filter(user = user_id).order_by("-created_at"),
        'url': f'/dashboard/0',
        'icon': 'fas fa-table',
        'title': 'Dashboard'
    }
    return render(request,'add_image.html',context)

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
def dashboard(request,image_id):
    if 'user_id' not in request.session:
        return redirect('/signin')
    else:
        current_user = User.objects.get(id=request.session['user_id'])
        if image_id != 0:
            current_image = Image.objects.get(id=image_id)
        else:
            current_image = 0;
        context = {
            'current_user': current_user,
            'users' : User.objects.all(),
            'images' : Image.objects.order_by("-created_at"),
            'current_image':current_image,
            'url': f'/users/add_image/{current_user.id}',
            'icon': 'fas fa-camera',
            'title': 'Post Image'
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

        return redirect(f'/dashboard/0')

#=============================================##
# process_edit_self()
# return redirect('/')
#=============================================##
def process_edit_self(request):
    return render(request,'process_edit_self.html')

#=============================================##
# process_add_image()
# return redirect('/')
#=============================================##
def process_add_image(request):
    post = request.POST

    upload_pet_form = UploadPetForm(request.POST, request.FILES)

    current_user = User.objects.get(id=request.session['user_id'])
    this_image = Image.objects.create(pet_img = request.FILES['pet_img'], user = current_user, name = post['name'], desc = post['desc'] )
    this_image.save()

    return redirect (f'/users/add_image/{current_user.id}')


#=============================================##
# process_remove_image()
# return redirect('/')
#=============================================##
def process_remove_image(request,image_id):
    post = request.POST
    user_id = request.session['user_id']
    this_image = Image.objects.get(id=image_id)
    this_image.delete()
    return redirect (f'/users/add_image/{user_id}')

#=============================================##
# process_add_comment()
# return redirect('/')
#=============================================##
def process_add_comment(request):
    post = request.POST
    print(request.POST)

    this_user = User.objects.get(id= request.session['user_id'])
    this_image = Image.objects.get(id = post['current_image_id'])
    new_comment = Comment.objects.create(text = post['text'], image = this_image, user= this_user)

    return redirect (f'/dashboard/{this_image.id}')


#=============================================##
# process_like()
# return redirect('/')
#=============================================##
def process_like_love(request,image_id,target_id):
    post = request.POST
    print(request.POST)
    
    this_user = User.objects.get(id= request.session['user_id'])
    this_image = Image.objects.get(id =image_id)

    if(target_id == 0):
        this_image.likes.add(this_user) 
    if(target_id == 1):
        this_image.loves.add(this_user) 

    this_image.save();

    return redirect (f'/dashboard/0')