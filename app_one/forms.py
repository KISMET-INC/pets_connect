from django import forms 
from .models import *


class UploadPetForm(forms.ModelForm): 
    class Meta:
        model = Image
        fields = ['pet_img']
        labels = {'pet_img': ''}

class UploadUserImgForm(forms.ModelForm): 
    class Meta:
        model = User
        fields = ['user_img']
        labels = {'user_img': ''}
