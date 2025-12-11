"""Views para autenticação."""
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from biblioteca.models import tbl_usuario
from django.conf import settings
from django.contrib.auth import logout

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        senha = request.POST.get("senha")

        usuario = authenticate(request, username=email, password=senha)

        if usuario is not None:
            login(request, usuario)
            return redirect('home')
        else:
            return render(request, 'auth/login.html', {
                'erro': 'Email ou senha inválidos'
            })

    return render(request, 'auth/login.html')

@login_required
def home(request):
    usuario_nome = request.user.nome
    return render(request, 'dashboard/home.html', {
        'usuario_nome': usuario_nome
    })
    
def logout_view(request):
    logout(request)        # limpa a sessão do usuário
    return redirect("/")   # volta para o login

def registro_view(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        sobrenome = request.POST.get("sobrenome")
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        senha2 = request.POST.get("senha2")

        if not nome or not sobrenome or not email or not senha:
            return render(request, "auth/registro.html", {
                "erro": "Preencha todos os campos."
            })

        if senha != senha2:
            return render(request, "auth/registro.html", {
                "erro": "As senhas não coincidem."
            })

        if tbl_usuario.objects.filter(email=email).exists():
            return render(request, "auth/registro.html", {
                "erro": "Este e-mail já está cadastrado."
            })

        usuario = tbl_usuario.objects.create(
            nome=nome,
            sobrenome=sobrenome,
            email=email,
            password=make_password(senha)
        )

        login(
        request,
        usuario,
        backend=settings.AUTHENTICATION_BACKENDS[0]
        )       
        return redirect("auth/login.html")

    return render(request, "auth/registro.html")
