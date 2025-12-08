"""Views para autenticação."""
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate

def login_view(request):
    """Processa login do usuário através de email."""
    if request.method == 'POST':
        email = request.POST.get("email")
        usuario = authenticate(request, email=email)
        
        if usuario is not None:
            request.session['usuario_id'] = usuario.id_usuario
            request.session['usuario_nome'] = usuario.nome
            request.session['usuario_sobrenome'] = usuario.sobrenome
            request.session['usuario_email'] = usuario.email
            return redirect('home')
        else:
            print("Usuário não encontrado ou credenciais inválidas")
    
    return render(request, 'auth/login.html')

def home(request):
    """Exibe a tela inicial após o login."""
    usuario_nome = request.session.get('usuario_nome', 'Visitante')
    return render(request, 'dashboard/home.html', {'usuario_nome': usuario_nome})