"""Views para gerenciamento de livros."""
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from ..forms import LivroCreateForm, LivroAutorForm, LivroCategoriaForm
from ..models import tbl_livro, tbl_livro_autor, tbl_livro_categoria, tbl_editora, tbl_autor, tbl_categoria

class LivroCreateView(View):
    """View para criar um novo livro."""
    template_name = "adicionar_livro.html"

    def get(self, request):
        form = LivroCreateForm(request.POST)
        editoras = tbl_editora.objects.all()

    def post(self, request):
        form = LivroCreateForm(request.POST)
        editoras = tbl_editora.objects.all()

        if not form.is_valid():
            print(form.errors)
            return render(request, self.template_name, {"form": form, "editoras": editoras})

        # Cria o livro
        livro = tbl_livro.objects.create(
            isbn=form.cleaned_data["isbn"],
            titulo=form.cleaned_data["titulo"],
            ano_publicacao=form.cleaned_data["ano_publicacao"],
            editora=form.cleaned_data["editora"],
            status=form.cleaned_data["status"]
        )

        # Autores
        for autor in form.cleaned_data["autores"]:
            tbl_livro_autor.objects.create(livro=livro, autor=autor)

        # Categorias
        for categoria in form.cleaned_data["categorias"]:
            tbl_livro_categoria.objects.create(livro=livro, categoria=categoria)

        return render(request, self.template_name, {
        "form": LivroCreateForm(), 
        "editoras": editoras,
        "sucesso": True,
        "livro_id": livro.id_livro,
        "livro_nome": livro.titulo
    })

def tela_todos_livros(request):
    """Exibe uma lista de todos os livros disponíveis na biblioteca."""
    livros = tbl_livro.objects.all()
    return render(request, 'tela_todos_os_livros.html', {'livros': livros})

class RemoverLivroView(View):
    """View para remover um livro."""
    def post(self, request, pk):
        livro = get_object_or_404(tbl_livro, pk=pk)
        livro.delete()
        return redirect('tela_todos_livros')

class AssociarAutorView(View):
    """View para associar autores a um livro."""
    template_name = "biblioteca/livro_autor_form.html"

    def get(self, request, pk):
        livro = get_object_or_404(tbl_livro, pk=pk)
        associados = tbl_autor.objects.filter(tbl_livro_autor__livro=livro)
        form = LivroAutorForm(initial={"autores": associados})
        
        return render(request, self.template_name, {
            "livro": livro,
            "form": form,
            "associados": associados
        })

    def post(self, request, pk):
        livro = get_object_or_404(tbl_livro, pk=pk)
        form = LivroAutorForm(request.POST)

        if form.is_valid():
            autores_selecionados = form.cleaned_data["autores"]
            tbl_livro_autor.objects.filter(livro=livro).delete()
            
            for autor in autores_selecionados:
                tbl_livro_autor.objects.create(livro=livro, autor=autor)

            return redirect("livro-detail", pk=livro.id_livro)

        return render(request, self.template_name, {
            "livro": livro,
            "form": form
        })

class AssociarCategoriaView(View):
    """View para associar categorias a um livro."""
    template_name = "biblioteca/livro_categoria_form.html"

    def get(self, request, pk):
        livro = get_object_or_404(tbl_livro, pk=pk)
        associadas = tbl_categoria.objects.filter(tbl_livro_categoria__livro=livro)
        form = LivroCategoriaForm(initial={"categorias": associadas})
        
        return render(request, self.template_name, {
            "livro": livro,
            "form": form,
            "associadas": associadas
        })

    def post(self, request, pk):
        livro = get_object_or_404(tbl_livro, pk=pk)
        form = LivroCategoriaForm(request.POST)

        if form.is_valid():
            categorias_selecionadas = form.cleaned_data["categorias"]
            tbl_livro_categoria.objects.filter(livro=livro).delete()
            
            for categoria in categorias_selecionadas:
                tbl_livro_categoria.objects.create(livro=livro, categoria=categoria)

            return redirect("livro-detail", pk=livro.id_livro)

        return render(request, self.template_name, {
            "livro": livro,
            "form": form
        })