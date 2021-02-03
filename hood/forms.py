from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from cloudinary.forms import CloudinaryFileField


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=300,help_text='Required. Inform a valid email address')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')



class UpdateUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'email')


class UpdateUserProfileForm(forms.ModelForm):
    profile_picture = CloudinaryFileField(
     options = { 
      'tags': "directly_uploaded",
      'crop': 'limit', 'width': 1000, 'height': 1000,
      'eager': [{ 'crop': 'fill', 'width': 150, 'height': 100 }]
    })
    class Meta:

        model = Profile
        fields = [ 'name','profile_picture', 'bio']

class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        image = CloudinaryFileField(
        options = { 
        'tags': "directly_uploaded",
        'crop': 'limit', 'width': 1000, 'height': 1000,
        'eager': [{ 'crop': 'fill', 'width': 150, 'height': 100 }]
        })
        widgets = {
          'description': forms.Textarea(attrs={'rows':4, 'cols':30}),
        }
        fields = ('name','address','email','image','description')

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        widgets = {
          'description': forms.Textarea(attrs={'rows':4, 'cols':30}),
        }
        fields = ('title','description')

