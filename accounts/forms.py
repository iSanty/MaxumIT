from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from ckeditor.fields import RichTextFormField


class MyUserCreationForm(UserCreationForm):
    username = forms.CharField(label='Usuario', max_length=30)
    email = forms.CharField()
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repetir Password', widget=forms.PasswordInput)
        
    class Meta:
        model = User
        fields = ['username', 'email', 'password1','password2']
        help_texts = {key: '' for key in fields}
        
        
class MyUserEditForm(forms.Form):
    email = forms.EmailField(required=False)
    first_name = forms.CharField(label='Nombre', max_length=30, required=False)
    last_name = forms.CharField(label='Apellido', max_length=30,required=False)
    descripcion = RichTextFormField()
    avatar = forms.ImageField(required=False)
    num_celular = forms.CharField()
    codigo_cliente = forms.IntegerField()
    
    
    
