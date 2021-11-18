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
