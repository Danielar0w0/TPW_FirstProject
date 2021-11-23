from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class PostForm(forms.Form):
    description = forms.CharField(max_length=256, widget=forms.Textarea(
        attrs={
            'id': 'description',
            'class': 'form-control',
            'rows': 5
        }
    ))
    file = forms.FileField(widget=forms.FileInput(
        attrs={
            'class': 'form-control',
            'id': 'file',
            'name': 'input_file',
            'accept': 'image/*'
        }
    ))


class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Email is required. Please insert a valid email.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class CommentForm(forms.Form):
    comment_content = forms.CharField(max_length=256, required=True, help_text='Please add a comment')


class DeletePostForm(forms.Form):
    post_id = forms.IntegerField()


class ProfileImageForm(forms.Form):
    image = forms.FileField(widget=forms.FileInput(
        attrs={
            'class': 'form-control',
            'id': 'image',
            'name': 'input_file',
            'accept': 'image/*'
        }
    ))


class ProfilePasswordForm(forms.Form):
    password = forms.CharField(max_length=80, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control'
        }
    ))


class MessageForm(forms.Form):

    content = forms.CharField(max_length=256, widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'rows': 4
        }
    ))
