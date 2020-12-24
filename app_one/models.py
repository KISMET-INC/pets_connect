from django.db import models
from datetime import *
import bcrypt
from django_resized import ResizedImageField
from django.db.models.signals import post_delete


class UserManager(models.Manager):

    #=============================================##
    # basic_validator SPECIFIC
    # validates the data for user registration
    #=============================================##
    def basic_validator(self, postData):
        post = postData
        print(postData)
        # empty error dictionary
        errors = {}

        # check password and confirm password match
        if post['pass'] != post['confirm']:
            errors['passmatch'] = 'Passwords do no match'
        # check password length
        if len(post['pass']) < 2:
            errors['passlen'] = 'Password must be at least 2 characters'
        
        if len(post['first']) < 2:
            errors['first'] = 'First Name bust be at least 2 characters'
        
        if len(post['email']) < 1:
            errors['email_format'] = 'Email must be correct format'

        # check unique email address
        users = User.objects.filter(email = postData['email'])
        print(users)
        if len(users) > 0:
            errors['email_in_use'] = 'Email already in use'
        
        return errors

    #=============================================##
    # basic_validator SPECIFIC LOGIN
    # validates the data for user registration
    #=============================================##
    def basic_validator_login(self, postData):
        post = postData
        print(postData)
        # empty error dictionary
        errors = {}

        if len(post['pass']) < 2:
            errors['passlen'] = 'Password must be at least 2 characters'
        
        if len(post['email']) < 2:
            errors['email'] = 'Email must be at least 2 characters and include @ sign'

        # check unique email address
        this_user = User.objects.filter(email = postData['email'])
    
        if len(this_user) == 0:
            errors['email_not_found'] = 'Email not in our database'
        else:
            verified_user = User.objects.get(id=this_user[0].id)
            if bcrypt.checkpw(post['pass'].encode(), verified_user.password.encode()) == False:
                errors['passcheck'] = 'Password does not match'
        return errors

    #=============================================##
    # basic_validator SPECIFIC PASSWORDS
    # validates the data for user registration
    #=============================================##
    def basic_validator_passwords(self, postData):
        post = postData
        print(postData)
        # empty error dictionary
        errors = {}

        if len(post['pass']) < 2:
            errors['passlen'] = 'Password must be at least 2 characters'
        
        if post['pass'] != post['confirm']:
            errors['passmatch'] = 'Passwords do no match'

        return errors

    
    #=============================================##
    # basic_validator SPECIFIC edit_user
    # validates the data for user registration
    #=============================================##
    def basic_validator_edit_user(self, postData):
        post = postData
        print(postData)
        # empty error dictionary
        errors = {}

        if len(post['first']) < 2:
            errors['first'] = 'First Name bust be at least 2 characters'
        
        if len(post['email']) < 1:
            errors['email_format'] = 'Email must be correct format'

        # check unique email address
        users = User.objects.filter(email = postData['email'])
        print(users)
        if len(users) > 0:
            if post['current_email'] != users[0].email:
                errors['email_in_use'] = 'Email already in use'

        return errors
        
#=============================================##
# MODEL CLASSES
#=============================================##

class User(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    user_name = models.CharField(max_length=30)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    user_level = models.IntegerField()
    ## USER.IMAGES (bucket)
    ## USER.COMMENTS (bucket)


class Image(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    pet_img = ResizedImageField(size=[300, 300], crop=['middle', 'center'], quality=100, force_format='png', upload_to='images/') 
    name = models.CharField(max_length=25)
    desc = models.CharField(max_length=255)

    loves = models.ManyToManyField(User, related_name="loves")
    likes = models.ManyToManyField(User, related_name="likes")
    user = models.ForeignKey(User, related_name= "images", on_delete = models.CASCADE)
    ## IMAGE.COMMENTS (bucket)



class Comment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    text = models.CharField(max_length=255)
    image = models.ForeignKey(Image, related_name="comments",on_delete = models.CASCADE)
    user = models.ForeignKey(User, related_name="comments",on_delete = models.CASCADE)
    