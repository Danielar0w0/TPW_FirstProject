from django import forms


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
