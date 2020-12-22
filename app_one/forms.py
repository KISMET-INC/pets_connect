from django import forms 
from .models import *


class UploadPetForm(forms.ModelForm): 


    class Meta:
        model = Image
        fields = ['pet_img']
        labels = {'pet_img': ''}
