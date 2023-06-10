from django.shortcuts import render

# Create your views here.


from django.shortcuts import redirect, render

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from .forms import MyUserCreationForm, MyUserEditForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from accounts.models import MasDatosUsuario



def conectarse(request):
    if request.method == "POST":
        form_login = AuthenticationForm(request, data=request.POST)
        
        if form_login.is_valid():
            username = form_login.cleaned_data.get('username')
            password = form_login.cleaned_data.get('password')
            
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                
                return redirect('inicio')
            else:
                return render(request, 'accounts/login.html', {'form': form_login})
        else:
            return render(request, 'accounts/login.html', {'form': form_login})
        
    form_login = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form_login})

@login_required
def registrarse(request):
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inicio')
        else:
            return render(request, 'accounts/registrarse.html', {'form':form})
        
    form = MyUserCreationForm()
    return render(request, 'accounts/registrarse.html', {'form':form})
        

@login_required
def perfil(request):
    return render(request, 'accounts/perfil.html')


@login_required
def editar_perfil(request):
    user = request.user
    mas_datos_usuario, _ = MasDatosUsuario.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        form = MyUserEditForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            if data.get('first_name'):
                user.first_name = data.get('first_name')
            if data.get('last_name'):
                user.last_name = data.get('last_name')
            if data.get('descripcion'):
                mas_datos_usuario.descripcion = data.get('descripcion')
            user.email = data.get('email') if data.get('email') else user.mail
            mas_datos_usuario.avatar = data.get('avatar') if data.get('avatar') else mas_datos_usuario.avatar
            mas_datos_usuario.save()
            user.save()
            return redirect('perfil')
        
        else:
            return render(request,'accounts/editar_perfil.html',{'form':form})
    form = MyUserEditForm(
        initial = {
            'email': user.email,
            'first_name': user.first_name,
            'last_name' : user.last_name,
            'avatar' : mas_datos_usuario.avatar,
            'descripcion': mas_datos_usuario.descripcion,
            
                    } )
    return render(request, 'accounts/editar_perfil.html',{'form':form})



class ChangePasswordView(PasswordChangeView):
    template_name = 'accounts/cambiar_password.html'
    success_url = '/accounts/perfil/'
    