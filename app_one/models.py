from django.db import models
from datetime import *
import bcrypt

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

        # check last name length
        if len(post['last']) < 2:
            errors['last'] = 'Last Name bust be at least 2 characters'
        
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

        # check last name length
        if len(post['last']) < 2:
            errors['last'] = 'Last Name bust be at least 2 characters'
        
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
    # basic_validator (GENERIC)
    # validates the data for user registration
    #=============================================##
    def basic_validator_generic(self, postData):
        # easy use variable
        post = postData
        # empty error dictionary
        errors = {}

        # check password and confirm password match
        if post['pass'] != post['confirm']:
            errors['passmatch'] = 'Passwords do no match'
        # check password length
        if len(post['pass']) < 2:
            errors['passlen'] = 'Password must be at least 8 characters'
        # check first name length
        if len(post['first']) < 2:
            errors['first'] = 'First Name bust be at least 2 characters'
        # check last name length
        if len(post['last']) < 2:
            errors['last'] = 'Last Name bust be at least 2 characters'

        # check unique email address
        users = User.objects.filter(email = postData['email'])
        if len(users) > 0:
            errors['email'] = 'Email already in use'

        # check appropriate age
        today = date.today()
            #date to year - cast as int
        this_year = int(today.strftime('%Y'))
        birth_year_str = post['bday']
            # slice out year - cast to int
        birth_year = int(birth_year_str[0:4])

        if this_year - 13 < birth_year:
            errors['age'] = 'You must be at least 13 years old'

        return errors



class User(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    user_level = models.IntegerField()
    ## USER.SENT MESSAGES (bucket)
    ## USER.RECIEVED MESSAGES (bucket)

class Message(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    text = models.CharField(max_length=255)
    user_to = models.ForeignKey(User, related_name = "recieved_messages",on_delete = models.CASCADE)
    user_from = models.ForeignKey(User, related_name= "sent_messages", on_delete = models.CASCADE)
    ## MESSAGE.COMMENTS (bucket)
    


class Comment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    text = models.CharField(max_length=255)
    message = models.ForeignKey(Message, related_name="comments",on_delete = models.CASCADE)