from django import forms
from django.forms import ModelForm, Textarea
from django.contrib.auth.models import User
from .models import Post, UserProfile

from easy_maps.widgets import AddressWithMapWidget



class PostForm(ModelForm):
        class Meta:
                model = Post
                fields = ['title','board','description','content','thumbImage',
'location']
                widgets = {'address': AddressWithMapWidget({'location':'vTextField'})}
                
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.CharField(max_length=255, required=True)
    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email', )

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture', )

class UserUpdateForm(forms.ModelForm):
    email = forms.CharField(max_length=255, required=True)
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', )


class UserPassUpdateForm(forms.Form):
    newPassword = forms.CharField(widget=forms.PasswordInput(), max_length=100)
    newPassword_confirm = forms.CharField(widget=forms.PasswordInput(), max_length=100)

