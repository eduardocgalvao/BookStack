"""Views para autenticação e gerenciamento de biblioteca."""

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate
from .forms import (
    CategoriaForm, 
    LivroCreateForm, 
    AutorForm, 
    EditoraForm,
    StatusLivroForm,
    UsuarioForm,
    MotivoRemocaoForm,
    LivroAutorForm,
    LivroCategoriaForm

)
from .models import (
    tbl_livro,
    tbl_autor,
    tbl_categoria,
    tbl_livro_autor,
    tbl_livro_categoria,
    tbl_editora,
    tbl_status_livro,
    tbl_usuario,
    tbl_motivo_remocao,
    tbl_livro_autor,
)


def login_view(request):
    """
    Processa login do usuário através de email.
    
    GET: Retorna formulário de login vazio.
    POST: Autentica usuário e armazena dados na sessão.
    """
    if request.method == 'POST':
        email = request.POST.get("email")
        
        # Autentica usando o backend customizado (TblUsuarioBackend)
        usuario = authenticate(request, email=email)
        
        if usuario is not None:
            # Armazena dados do usuário na sessão
            request.session['usuario_id'] = usuario.id_usuario
            request.session['usuario_nome'] = usuario.nome
            request.session['usuario_sobrenome'] = usuario.sobrenome
            request.session['usuario_email'] = usuario.email
            return redirect('tela_inicial')
        else:
            print("Usuário não encontrado ou credenciais inválidas")
    
    return render(request, 'login.html')

def tela_inicial(request):
    """
    Exibe a tela inicial após o login.
    Mostra informações básicas do usuário logado.
    """
    usuario_nome = request.session.get('usuario_nome', 'Visitante')
    
    context = {
        'usuario_nome': usuario_nome,
    }
    
    return render(request, 'tela_inicial.html', context)

def tela_todos_livros(request):
    """
    Exibe uma lista de todos os livros disponíveis na biblioteca.
    """
    livros = tbl_livro.objects.all()
    return render(request, 'tela_todos_os_livros.html', {'livros': livros})

def adicionar_livro(request):
    """
    View para adicionar um novo livro ao acervo.
    
    GET: Exibe o formulário de criação de livro.
    POST: Processa o formulário e cria o livro no banco de dados.
    """
    if request.method == 'POST':
        form = LivroCreateForm(request.POST)
        if form.is_valid():
            livro = tbl_livro.objects.create(
                isbn=form.cleaned_data['isbn'],
                titulo=form.cleaned_data['titulo'],
                ano_publicacao=form.cleaned_data['ano_publicacao'],
                editora=form.cleaned_data['editora'],
                status=form.cleaned_data['status']
            )
            # Salvar autores na tabela through
            for autor in form.cleaned_data["autores"]:
                tbl_livro_autor.objects.create(
                    livro=livro, 
                    autor=autor
                )
            # Salvar categorias na tabela through
            for categoria in form.cleaned_data["categorias"]:
                tbl_livro_categoria.objects.create(
                    livro=livro,
                    categoria=categoria
                )
            return redirect('tela_inicial')
    else:
        form = LivroCreateForm()
    
    return render(request, 'adicionar_livro.html', {'form': form})

def adicionar_autor(request):
    """
    View para adicionar um novo autor.
    
    GET: Exibe o formulário de criação de autor.
    POST: Processa o formulário e cria o autor no banco de dados.
    """
    if request.method == 'POST':
        form = AutorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tela_inicial')
    else:
        form = AutorForm()
    
    return render(request, 'adicionar_autor.html', {'form': form})

# CRIAR LIVRO ----------------------------------------------------------
class LivroCreateView(View):
    template_name = "adicionar_livro.html"

    def get(self, request):
        form = LivroCreateForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = LivroCreateForm(request.POST)

        # 1) Processa o formulário de criação de livro
        if form.is_valid():
            livro = tbl_livro.objects.create(
                isbn=form.cleaned_data['isbn'],
                titulo=form.cleaned_data['titulo'],
                ano_publicacao=form.cleaned_data['ano_publicacao'],
                editora=form.cleaned_data['editora'],
                status=form.cleaned_data['status']
            )

        # 2) Salvar autores na tabela through
        for autor in form.cleaned_data["autores"]:
            tbl_livro_autor.objects.create(
            livro=livro, 
            autor=autor
        )
        # 3) Salvar categorias na tabela through
        for categoria in form.cleaned_data["categorias"]:
            tbl_livro_categoria.objects.create(
                livro=livro,
                categoria=categoria
            )

        return redirect("livro_list")  # Redireciona para a lista de livros após criação
        return render(request, self.template_name,{'form': form})
    
#CRIAR AUTOR ----------------------------------------------------------

class AutorCreateView(View):
    template_name = "biblioteca/autor_form.html"
    
    def get(self, request):
        form = AutorForm()
        return render(request, self.template_name, {'form': form})
        
    def post(self, request):
        form = AutorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("autor_list")  # Redireciona para a lista de autores após criação
        return render(request, self.template_name, {'form': form})

# LISTAR AUTORES ------------------------------------------------------

class AutorListView(View):
    template_name = "biblioteca/autor_list.html"

    def get(self, request):
        autores = tbl_autor.objects.all()
        return render(request, self.template_name, {"autores": autores})
    
# EDITAR AUTOR --------------------------------------------------------

class AutorUpdateView(View):
    template_name = "biblioteca/autor_form.html"

    def get(self, request, pk):
        autor = get_object_or_404(tbl_autor, pk=pk)
        form = AutorForm(instance=autor)
        return render(request, self.template_name, {"form": form, "autor": autor})

    def post(self, request, pk):
        autor = get_object_or_404(tbl_autor, pk=pk)
        form = AutorForm(request.POST, instance=autor)
        if form.is_valid():
            form.save()
            return redirect("autor-list")
        return render(request, self.template_name, {"form": form, "autor": autor})
    
# DELETAR AUTOR --------------------------------------------------------
class AutorDeleteView(View):
    template_name = "biblioteca/autor_confirm_delete.html"

    def get(self, request, pk):
        autor = get_object_or_404(tbl_autor, pk=pk)
        return render(request, self.template_name, {"autor": autor})

    def post(self, request, pk):
        autor = get_object_or_404(tbl_autor, pk=pk)
        autor.delete()
        return redirect("autor-list")

# LISTAR CATEGORIAS --------------------------------------------------------

class CategoriaListView(View):
    template_name = "biblioteca/categoria_list.html"

    def get(self, request):
        categorias = tbl_categoria.objects.all()
        return render(request, self.template_name, {"categorias": categorias})


# CRIAR CATEGORIA ----------------------------------------------------------

class CategoriaCreateView(View):
    template_name = "biblioteca/categoria_form.html"

    def get(self, request):
        form = CategoriaForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("categoria-list")
        return render(request, self.template_name, {"form": form})


# EDITAR CATEGORIA ---------------------------------------------------------

class CategoriaUpdateView(View):
    template_name = "biblioteca/categoria_form.html"

    def get(self, request, pk):
        categoria = get_object_or_404(tbl_categoria, pk=pk)
        form = CategoriaForm(instance=categoria)
        return render(request, self.template_name, {"form": form, "categoria": categoria})

    def post(self, request, pk):
        categoria = get_object_or_404(tbl_categoria, pk=pk)
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect("categoria-list")
        return render(request, self.template_name, {"form": form, "categoria": categoria})


# DELETAR CATEGORIA --------------------------------------------------------

class CategoriaDeleteView(View):
    template_name = "biblioteca/categoria_confirm_delete.html"

    def get(self, request, pk):
        categoria = get_object_or_404(tbl_categoria, pk=pk)
        return render(request, self.template_name, {"categoria": categoria})

    def post(self, request, pk):
        categoria = get_object_or_404(tbl_categoria, pk=pk)
        categoria.delete()
        return redirect("categoria-list")

# LISTAR EDITORAS --------------------------------------------------------

class EditoraListView(View):
    template_name = "biblioteca/editora_list.html"

    def get(self, request):
        editoras = tbl_editora.objects.all()
        return render(request, self.template_name, {"editoras": editoras})


# CRIAR EDITORA ----------------------------------------------------------

class EditoraCreateView(View):
    template_name = "biblioteca/editora_form.html"

    def get(self, request):
        form = EditoraForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = EditoraForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("editora-list")
        return render(request, self.template_name, {"form": form})


# EDITAR EDITORA ---------------------------------------------------------

class EditoraUpdateView(View):
    template_name = "biblioteca/editora_form.html"

    def get(self, request, pk):
        editora = get_object_or_404(tbl_editora, pk=pk)
        form = EditoraForm(instance=editora)
        return render(request, self.template_name, {"form": form, "editora": editora})

    def post(self, request, pk):
        editora = get_object_or_404(tbl_editora, pk=pk)
        form = EditoraForm(request.POST, instance=editora)
        if form.is_valid():
            form.save()
            return redirect("editora-list")
        return render(request, self.template_name, {"form": form, "editora": editora})


# DELETAR EDITORA ---------------------------------------------------------

class EditoraDeleteView(View):
    template_name = "biblioteca/editora_confirm_delete.html"

    def get(self, request, pk):
        editora = get_object_or_404(tbl_editora, pk=pk)
        return render(request, self.template_name, {"editora": editora})

    def post(self, request, pk):
        editora = get_object_or_404(tbl_editora, pk=pk)
        editora.delete()
        return redirect("editora-list")
    
# LISTAR STATUS --------------------------------------------------------

class StatusLivroListView(View):
    template_name = "biblioteca/status_list.html"

    def get(self, request):
        status_list = tbl_status_livro.objects.all()
        return render(request, self.template_name, {"status_list": status_list})


# CRIAR STATUS ---------------------------------------------------------

class StatusLivroCreateView(View):
    template_name = "biblioteca/status_form.html"

    def get(self, request):
        form = StatusLivroForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = StatusLivroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("status-list")
        return render(request, self.template_name, {"form": form})


# EDITAR STATUS --------------------------------------------------------

class StatusLivroUpdateView(View):
    template_name = "biblioteca/status_form.html"

    def get(self, request, pk):
        status_item = get_object_or_404(tbl_status_livro, pk=pk)
        form = StatusLivroForm(instance=status_item)
        return render(request, self.template_name, {"form": form, "status_item": status_item})

    def post(self, request, pk):
        status_item = get_object_or_404(tbl_status_livro, pk=pk)
        form = StatusLivroForm(request.POST, instance=status_item)
        if form.is_valid():
            form.save()
            return redirect("status-list")
        return render(request, self.template_name, {"form": form, "status_item": status_item})


# DELETAR STATUS --------------------------------------------------------

class StatusLivroDeleteView(View):
    template_name = "biblioteca/status_confirm_delete.html"

    def get(self, request, pk):
        status_item = get_object_or_404(tbl_status_livro, pk=pk)
        return render(request, self.template_name, {"status_item": status_item})

    def post(self, request, pk):
        status_item = get_object_or_404(tbl_status_livro, pk=pk)
        status_item.delete()
        return redirect("status-list")
    
# LISTAR USUÁRIOS --------------------------------------------------------

class UsuarioListView(View):
    template_name = "biblioteca/usuario_list.html"

    def get(self, request):
        usuarios = tbl_usuario.objects.all()
        return render(request, self.template_name, {"usuarios": usuarios})


# CRIAR USUÁRIO ----------------------------------------------------------

class UsuarioCreateView(View):
    template_name = "biblioteca/usuario_form.html"

    def get(self, request):
        form = UsuarioForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("usuario-list")
        return render(request, self.template_name, {"form": form})


# EDITAR USUÁRIO ---------------------------------------------------------

class UsuarioUpdateView(View):
    template_name = "biblioteca/usuario_form.html"

    def get(self, request, pk):
        usuario = get_object_or_404(tbl_usuario, pk=pk)
        form = UsuarioForm(instance=usuario)
        return render(request, self.template_name, {"form": form, "usuario": usuario})

    def post(self, request, pk):
        usuario = get_object_or_404(tbl_usuario, pk=pk)
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect("usuario-list")
        return render(request, self.template_name, {"form": form, "usuario": usuario})


# DELETAR USUÁRIO ---------------------------------------------------------

class UsuarioDeleteView(View):
    template_name = "biblioteca/usuario_confirm_delete.html"

    def get(self, request, pk):
        usuario = get_object_or_404(tbl_usuario, pk=pk)
        return render(request, self.template_name, {"usuario": usuario})

    def post(self, request, pk):
        usuario = get_object_or_404(tbl_usuario, pk=pk)
        usuario.delete()
        return redirect("usuario-list")

# LISTAR MOTIVOS --------------------------------------------------------

class MotivoRemocaoListView(View):
    template_name = "biblioteca/motivo_list.html"

    def get(self, request):
        motivos = tbl_motivo_remocao.objects.all()
        return render(request, self.template_name, {"motivos": motivos})


# CRIAR MOTIVO ----------------------------------------------------------

class MotivoRemocaoCreateView(View):
    template_name = "biblioteca/motivo_form.html"

    def get(self, request):
        form = MotivoRemocaoForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = MotivoRemocaoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("motivo-list")
        return render(request, self.template_name, {"form": form})


# EDITAR MOTIVO ---------------------------------------------------------

class MotivoRemocaoUpdateView(View):
    template_name = "biblioteca/motivo_form.html"

    def get(self, request, pk):
        motivo = get_object_or_404(tbl_motivo_remocao, pk=pk)
        form = MotivoRemocaoForm(instance=motivo)
        return render(request, self.template_name, {"form": form, "motivo": motivo})

    def post(self, request, pk):
        motivo = get_object_or_404(tbl_motivo_remocao, pk=pk)
        form = MotivoRemocaoForm(request.POST, instance=motivo)
        if form.is_valid():
            form.save()
            return redirect("motivo-list")
        return render(request, self.template_name, {"form": form, "motivo": motivo})


# EXCLUIR MOTIVO ---------------------------------------------------------

class MotivoRemocaoDeleteView(View):
    template_name = "biblioteca/motivo_confirm_delete.html"

    def get(self, request, pk):
        motivo = get_object_or_404(tbl_motivo_remocao, pk=pk)
        return render(request, self.template_name, {"motivo": motivo})

    def post(self, request, pk):
        motivo = get_object_or_404(tbl_motivo_remocao, pk=pk)
        motivo.delete()
        return redirect("motivo-list")

# ASSOCIAÇÃO DE AUTORES -----------------------------------------------------

class AssociarAutorView(View):
    template_name = "biblioteca/livro_autor_form.html"

    def get(self, request, pk):
        livro = get_object_or_404(tbl_livro, pk=pk)

     # autores já associados ao livro
        associados = tbl_autor.objects.filter(tbl_livro_autor__livro=livro)

        form = LivroAutorForm(initial={
            "autores": associados
        }
    )

        return render(request, self.template_name, {
            "livro": livro,
            "form": form,
            "associados": associados
        }
    )

    def post(self, request, pk):
        livro = get_object_or_404(tbl_livro, pk=pk)
        form = LivroAutorForm(request.POST)

        if form.is_valid():
            autores_selecionados = form.cleaned_data["autores"]

            # remove associações antigas
            tbl_livro_autor.objects.filter(livro=livro).delete()

            # cria novas associações
            for autor in autores_selecionados:
                tbl_livro_autor.objects.create(
                    livro=livro,
                    autor=autor
                )

            return redirect("livro-detail", pk=livro.id_livro)

        # caso haja erro, renderizar de novo
        return render(request, self.template_name, {
            "livro": livro,
            "form": form
        }
    )

# VIEW DA ASSOCIAÇÃO DE CATEGORIAS -----------------------------------------------------

class AssociarCategoriaView(View):
    template_name = "biblioteca/livro_categoria_form.html"

    def get(self, request, pk):
        livro = get_object_or_404(tbl_livro, pk=pk)

        # categorias já associadas
        associadas = tbl_categoria.objects.filter(tbl_livro_categoria__livro=livro)

        form = LivroCategoriaForm(initial={
            "categorias": associadas
        }
    )

        return render(request, self.template_name, {
            "livro": livro,
            "form": form,
            "associadas": associadas
        }
    )

    def post(self, request, pk):
        livro = get_object_or_404(tbl_livro, pk=pk)
        form = LivroCategoriaForm(request.POST)

        if form.is_valid():
            categorias_selecionadas = form.cleaned_data["categorias"]

            # remove associações antigas
            tbl_livro_categoria.objects.filter(livro=livro).delete()

            # cria novas associações
            for categoria in categorias_selecionadas:
                tbl_livro_categoria.objects.create(
                    livro=livro,
                    categoria=categoria
                )

            return redirect("livro-detail", pk=livro.id_livro)

        return render(request, self.template_name, {
            "livro": livro,
            "form": form
        }
    )
