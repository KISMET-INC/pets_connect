from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.db.models import Sum
from .models import *
import bcrypt
from .forms import *

#=============================================##
# process_register()
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
            return redirect(f'/explore')

        return redirect(f'/explore')

#=============================================##
# process_signin()
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
            return redirect(f'/explore')


#=============================================##
# logout()
#=============================================##
def logout(request):
    request.session.flush()
    return redirect('/')



#=============================================##
# home()
#=============================================##
def landing(request):
    return render(request,'landing.html')

#=============================================##
# signin()
#=============================================##
def signin(request):
    return render(request,'signin.html')

#=============================================##
# register()
#=============================================##
def register(request):
    return render(request,'register.html')

#=============================================##
# admin()
#=============================================##
def admin(request):
    context = {
        'users': User.objects.all()
    }
    return render(request,'admin.html',context)
    


#=============================================##
# explore()
#=============================================##
def explore(request):

    if 'user_id' not in request.session:
        return redirect('/signin')    
    current_user = User.objects.get(id=request.session['user_id'])
    context = {
        'session_user': current_user,
        'users' : User.objects.all(),
        'images' : Image.objects.order_by("-created_at"),
        'location': 'explore',
        'icon': 'fas fa-cloud-upload-alt',
        'title': 'Share',
    }

    if request.session['user_level'] == 0:
        return render(request,'explore.html',context)
    return render(request,'admin.html',context)


#=============================================##
# profile()
#=============================================##
def profile(request, user_id):
    session_user = User.objects.get(id=request.session['user_id'])
    images = Image.objects.filter(user = user_id).order_by("-created_at");

    heart_sum = 0
    for image in images:
        heart_sum += image.loves.count()

    context = {
        'upload_pet_form': UploadPetForm(),
        'session_user': session_user,
        'clicked_user' : User.objects.get(id=user_id),
        'images': images,
        'icon': 'fas fa-table',
        'title': 'explore',
        'location': 'profile',
        'heart_sum': heart_sum,
    }
    return render(request,'profile.html',context)

#=============================================##
# edit_user() VIEW
#=============================================##
def edit_user(request,user_id):
    context = {
        'session_user' : User.objects.get(id=request.session['user_id']),
        'user_upload_img' : UploadUserImgForm(),
    }
    return render(request,'edit_user.html',context)
    

#=============================================##
# process_edit_user()
#=============================================##
def process_edit_user(request):
    session_user = User.objects.get(id=request.session['user_id'])
    user_upload_img = UploadUserImgForm(request.POST, request.FILES)
        
    session_user.email = request.POST['email']
    session_user.user_name = request.POST['user_name']

    if request.FILES:
        session_user.user_img = request.FILES['user_img']
    session_user.save()

    return redirect(f'/profile/{session_user.id}')



#=============================================##
# admin_edit_user() VIEW
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
# process_admin_remove_user()
#=============================================##
def process_remove_user(request, user_id):
    this_user = User.objects.get(id = user_id)
    this_user.delete()
    return redirect('/explore/0')



#=============================================##
# bulletin()
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
# process_add_pet_image()
# return redirect('/')
#=============================================##
def process_add_pet_image(request):

    upload_pet_form = UploadPetForm(request.POST, request.FILES)
    session_user = User.objects.get(id=request.session['user_id'])
    this_image = Image.objects.create(pet_img = request.FILES['pet_img'], user = session_user, name = request.POST['name'], desc = request.POST['desc'] )
    this_image.save()

    return redirect (f'/profile/{session_user.id}')


#=============================================##
# process_remove_pet_image()
#=============================================##
def process_remove_image(request,image_id):
    session_user = User.objects.get(id=request.session['user_id'])
    this_image = Image.objects.get(id=image_id)
    this_user = User.objects.get(id = this_image.user.id)
    this_image.delete()
    if session_user.user_level == 9:
        return redirect (f'/admin_edit_user/{this_user.id}')
    return redirect (f'/profile/{session_user.id}')

#=============================================##
# process_add_comment()
#=============================================##
def process_add_comment(request):
    print('post request')
    print(request.POST)
    session_user = User.objects.get(id= request.session['user_id'])
    this_image = Image.objects.get(id = request.POST['image_id'])
    new_comment = Comment.objects.create(text = request.POST['text'], image = this_image, user= session_user)
    context = {
        'image': this_image,
        'session_user': session_user
    }
    #hidden form field
    if request.POST['component'] == 'from_post':
        return redirect(f'/replace_post/{this_image.id}')
    return redirect( f'/replace_comments/{this_image.id}')


#=============================================##
# process_delete_comment()
#=============================================##
def process_delete_comment(request,comment_id,component):
    session_user = User.objects.get(id= request.session['user_id'])
    this_comment = Comment.objects.get(id = comment_id)
    image_id = this_comment.image.id
    clicked_user = this_comment.user
    this_comment.delete();
    if component == 'from_post':
        print(image_id)
        return redirect(f'/replace_post/{image_id}')
    return redirect(f'/replace_comments/{image_id}')

#=============================================##
# replace_comments() 
#=============================================##
def replace_comments(request, image_id):
    session_user = User.objects.get(id= request.session['user_id'])
    this_image = Image.objects.get(id = image_id)
    context = {
        'image': this_image,
        'session_user': session_user
    }
    return render(request, 'modules/modal_comments.html', context)


#=============================================##
# replace_post()
#=============================================##
def replace_post(request, image_id):
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
        return redirect(f'/replace_post/{this_image.id}')

    return redirect(f'/replace_stats/{this_image.id}')


#=============================================##
# replace stats
#=============================================##
def replace_stats(request, image_id):
    print('im here in updated stats')
    session_user = User.objects.get(id=request.session['user_id'])
    this_image = Image.objects.get(id=image_id)
    context = {
        'image': this_image,
        'session_user': session_user
    }
    return render(request,'modules/stats.html', context)


#=============================================##
# replace image
#=============================================##
def replace_image(request, image_id):
    print('im here in updated stats')
    session_user = User.objects.get(id=request.session['user_id'])
    this_image = Image.objects.get(id=image_id)
    context = {
        'image': this_image,
        'session_user': session_user
    }
    return render(request,'modules/image.html', context)




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
        return redirect(f'/profile/{user_to_follow_id}')

    return redirect (f'/explore')


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
    return redirect (f'/profile/{clicked_user.id}')


#=============================================##
# get_session_id()
#=============================================##
def get_session_id(request):
    session_id = request.session['user_id']
    return HttpResponse (session_id)



    
#=============================================##
# process_edit_password()
# NOT BEING USED YET
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
   