"""Views para autenticação."""
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        senha = request.POST.get("senha")

        usuario = authenticate(request, username=email, password=senha)

        if usuario is not None:
            login(request, usuario)

            request.session['usuario_id'] = usuario.id_usuario
            request.session['usuario_nome'] = usuario.nome
            request.session['usuario_sobrenome'] = usuario.sobrenome
            request.session['usuario_email'] = usuario.email

            return redirect('home')
        else:
            return render(request, 'auth/login.html', {
                'erro': 'Email ou senha inválidos'
            })

    return render(request, 'auth/login.html')

@login_required
def home(request):
    usuario_nome = request.user.nome or request.user.email
    return render(request, 'dashboard/home.html', {
        'usuario_nome': usuario_nome
    })