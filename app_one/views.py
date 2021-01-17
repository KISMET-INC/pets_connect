from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.db.models import Sum
from .models import *
import bcrypt
from .forms import *


#=============================================##
# process_remove_user()
# PROCESSES the deletion of a user in the
# database.  REDIRECTS to read_all table
#=============================================##
def process_remove_user(request, user_id):
    this_user = User.objects.get(id = user_id)
    this_user.delete()
    return redirect('/explore/0')


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
            return redirect('/explore/admin')
        
        if new_user.user_level != 9:
            kristen = User.objects.get(id=2)
            new_user.is_following.add(kristen)
            kristen.being_followed.add(new_user)
            new_user.being_followed.add(kristen)
            kristen.save()
            new_user.save()

        if user_level not in request.session:
            request.session['user_id'] = new_user.id
            request.session['user_name'] = new_user.user_name
            request.session['user_level'] = new_user.user_level
            return redirect(f'/explore/{new_user.id}/0/0')

        return redirect(f'/explore/{new_user.id}/0/0')




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
    user = User.objects.filter(email = request.POST['email'])
    errors = User.objects.basic_validator_login(request.POST)

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
                return redirect('explore/admin')
            return redirect(f'/explore/{this_user.id}/0/0')





#=============================================##
# home()
#
#=============================================##
def landing(request):
    return render(request,'landing.html')

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
# profile()
#
#=============================================##
def profile(request, user_id, image_id, modal_trigger):
    session_user = User.objects.get(id=request.session['user_id'])
    if image_id != 0:
        current_image = Image.objects.get(id=image_id)
    else:
        current_image = 0
    images = Image.objects.filter(user = user_id).order_by("-created_at");

    heart_sum = 0
    for image in images:
        heart_sum += image.loves.count()

    context = {

        'upload_pet_form': UploadPetForm(),
        'session_user': session_user,
        'clicked_user' : User.objects.get(id=user_id),
        'images': images,
        'image': current_image,
        'icon': 'fas fa-table',
        'title': 'explore',
        'location': 'profile',
        'trigger': modal_trigger,
        'heart_sum': heart_sum,
    }
    return render(request,'profile.html',context)

#=============================================##
# edit_user()
#
#=============================================##
def edit_user(request,user_id):
    context = {
        'session_user' : User.objects.get(id=request.session['user_id']),
        'user_upload_img' : UploadUserImgForm(),
    }
    return render(request,'edit_user.html',context)


#=============================================##
# admin_edit_user()
#
#=============================================##
def admin_edit_user(request,user_id,image_id,modal_trigger):
    if image_id != 0:
        image = Image.objects.get(id=image_id)
    else:
        image = image_id

    context = {
        'session_user' : User.objects.get(id=request.session['user_id']),
        'image': image,
        'trigger': modal_trigger,
        'clicked_user' : User.objects.get(id=user_id),
        'user_upload_img' : UploadUserImgForm(),
        'location': 'admin_edit_user',

    }
    return render(request,'admin_edit_user.html',context)

    
#=============================================##
# admin_add_user()
#
#=============================================##
def admin_add_user(request):
    context = {
        'session_user' : User.objects.get(id=request.session['user_id']),
        'user' : User.objects.get(id=user_id),
        'user_upload_img' : UploadUserImgForm(),
    }
    return render(request,'admin_add_user.html',context)

    

    
#=============================================##
# bulletin()
#
#=============================================##
def bulletin(request,user_id,image_id, modal_trigger):
    if image_id != 0:
        current_image = Image.objects.get(id=image_id)
    else:
        current_image = 0;

    context = {
        'session_user': User.objects.get(id=request.session['user_id']),
        'selected_user': User.objects.get(id=user_id),
        'url' : f'/user/bulletin/{user_id}/{image_id}',
        'image': current_image,
        'images': Image.objects.order_by("-created_at"),
        'location': 'bulletin',
        'trigger': modal_trigger,
        'comments': Comment.objects.filter(image = current_image).order_by('-created_at'),
    }
    return render(request,'bulletin.html',context)


#=============================================##
# explore()
#
#=============================================##
def explore(request, user_id,image_id,modal_trigger):

    if 'user_id' not in request.session:
        return redirect('/signin')

    
    current_user = User.objects.get(id=request.session['user_id'])
    if image_id != 0:
        current_image = Image.objects.get(id=image_id)
    else:
        current_image = 0;
    context = {
        'session_user': current_user,
        'users' : User.objects.all(),
        'images' : Image.objects.order_by("-created_at"),
        'image':current_image,
        'location': 'explore',
        'icon': 'fas fa-cloud-upload-alt',
        'title': 'Share',
        'trigger': modal_trigger
    }

    if request.session['user_level'] == 0:
        return render(request,'explore.html',context)
    return render(request,'admin.html',context)



#=============================================##
# process_edit_password()
# return redirect('/')
#=============================================##
def process_edit_password(request):
    errors = User.objects.basic_validator_passwords(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/edit_user/{request.POST["user_id"]}')
    else:
        session_user = User.objects.get(id=request.POST['user_id'])
        session_user.password = request.POST['pass']

        
    return redirect(f'/edit_user/{session_user.id}')


    

#=============================================##
# process_edit_user()
# return redirect('/')
#=============================================##
def process_edit_user(request):
    session_user = User.objects.get(id=request.session['user_id'])
    user_upload_img = UploadUserImgForm(request.POST, request.FILES)
        
    session_user.email = request.POST['email']
    session_user.user_name = request.POST['user_name']
    if request.FILES:
        session_user.user_img = request.FILES['user_img']
    session_user.save()

    return redirect(f'/profile/{session_user.id}/0/0')


#=============================================##
# process_admin_edit_user()
# return redirect('/')
#=============================================##
def process_admin_edit_user(request, user_id):
    user = User.objects.get(id=user_id)
    user_upload_img = UploadUserImgForm(request.POST, request.FILES)
        
    user.email = request.POST['email']
    user.user_name = request.POST['user_name']
    if request.FILES:
        user.user_img = request.FILES['user_img']
    user.save()

    return redirect(f'/admin_edit_user/{user_id}')


#=============================================##
# process_add_image()
# return redirect('/')
#=============================================##
def process_add_image(request):

    upload_pet_form = UploadPetForm(request.POST, request.FILES)
    session_user = User.objects.get(id=request.session['user_id'])
    this_image = Image.objects.create(pet_img = request.FILES['pet_img'], user = session_user, name = request.POST['name'], desc = request.POST['desc'] )
    this_image.save()

    return redirect (f'/profile/{session_user.id}/0/0')


#=============================================##
# process_remove_image()
# return redirect('/')
#=============================================##
def process_remove_image(request,image_id,location):
    session_user = User.objects.get(id=request.session['user_id'])
    this_image = Image.objects.get(id=image_id)
    this_user = User.objects.get(id = this_image.user.id)
    this_image.delete()
    if session_user.user_level == 9:
        return redirect (f'/admin_edit_user/{this_user.id}')
    return redirect (f'/{location}/{session_user.id}/0/0')

#=============================================##
# process_add_comment()
# return redirect('/')
#=============================================##
def process_add_comment(request):
    print(request.POST)
    session_user = User.objects.get(id= request.session['user_id'])
    this_image = Image.objects.get(id = request.POST['image_id'])
    new_comment = Comment.objects.create(text = request.POST['text'], image = this_image, user= session_user)
    context = {
        'image': this_image,
        'session_user': session_user
    }
    if request.POST['component'] == 'post':
        return render(request,'modules/post.html', context)
    return redirect( f'/updated_comments/{this_image.id}')


#=============================================##
# process_delete_comment()
#=============================================##
def process_delete_comment(request,comment_id):
    session_user = User.objects.get(id= request.session['user_id'])
    this_comment = Comment.objects.get(id = comment_id)
    image_id = this_comment.image.id
    clicked_user = this_comment.user
    this_comment.delete();
    return redirect(f'/updated_comments/{image_id}')

#=============================================##
# updated_comments() 
#=============================================##
def updated_comments(request, image_id):
    session_user = User.objects.get(id= request.session['user_id'])
    this_image = Image.objects.get(id = image_id)
    print('here')
    context = {
        'image': this_image,
        'session_user': session_user
    }
    return render(request, 'modules/modal_comments.html', context)


#=============================================##
# updated_post()
#=============================================##
def updated_post(request, image_id):
    session_user = User.objects.get(id=request.session['user_id'])
    this_image = Image.objects.get(id=image_id)
    context = {
        'image': this_image,
        'session_user': session_user
    }
    return render(request,'modules/post.html', context)

#=============================================##
# replace_modal()
#=============================================##
def replace_modal(request, image_id):
    context = {
        'image' : Image.objects.get(id=image_id),
        'session_user' : User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'modules/modal.html', context)






#=============================================##
# process_heart()
#=============================================##
def process_heart(request,image_id,location):
    
    session_user = User.objects.get(id=request.session['user_id'])
    this_image = Image.objects.get(id=image_id)

    if session_user in this_image.loves.all():
        this_image.loves.remove(session_user) 
    else:
        this_image.loves.add(session_user) 
    
    this_image.save();

    if location == 'bulletin':
        return redirect(f'/updated_post/{this_image.id}')

    return redirect(f'/updated_stats/{this_image.id}')

def updated_stats(request, image_id):
    print('im here in updated stats')
    session_user = User.objects.get(id=request.session['user_id'])
    this_image = Image.objects.get(id=image_id)
    context = {
        'image': this_image,
        'session_user': session_user
    }
    return render(request,'modules/stats.html', context)




#=============================================##
# process_follow()
# return redirect('/')
#=============================================##
def process_follow(request,image_id,user_to_follow_id,location):

    session_user = User.objects.get(id= request.session['user_id'])
    user_to_follow = User.objects.get(id= user_to_follow_id)

    session_user.is_following.add(user_to_follow);
    user_to_follow.being_followed.add(session_user);
    session_user.save()
    user_to_follow.save()
    if location == 'profile':
        return redirect(f'/profile/{user_to_follow_id}/0/1')

    return redirect (f'/explore/{session_user.id}/0/0')

#=============================================##
# process_follow()
# return redirect('/')
#=============================================##
def comment_frame(request, image_id):
    image = Image.objects.get(id=image_id)
    session_user = User.objects.get(id= request.session['user_id'])

    context ={
        'session_user': session_user,
        'comments': Comment.objects.filter(image = image).order_by('-created_at'),
        'location': 'comment_frame',
        'image': image
    }
    return render(request,'comment_frame.html',context)




#=============================================##
# stop_following()
# return redirect('/')
#=============================================##
def stop_following(request, user_id):
    session_user = User.objects.get(id= request.session['user_id'])
    clicked_user = User.objects.get(id= user_id)
    session_user.is_following.remove(clicked_user)
    clicked_user.being_followed.remove(session_user)
    session_user.save()
    clicked_user.save()
    return redirect (f'/profile/{clicked_user.id}/0/0')

#=============================================##
# get_session_id()
#=============================================##
def get_session_id(request):
    session_id = request.session['user_id']
    return HttpResponse (session_id)