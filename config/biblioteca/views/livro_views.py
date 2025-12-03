"""Views para gerenciamento de livros."""
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from django.views import View
from ..forms import LivroCreateForm, LivroAutorForm, LivroCategoriaForm
from ..models import tbl_livro, tbl_livro_autor, tbl_livro_categoria, tbl_editora, tbl_autor, tbl_categoria


# Para todos os livros sem data_criacao
livros_sem_data = tbl_livro.objects.filter(dt_criacao__isnull=True)
for livro in livros_sem_data:
    livro.dt_criacao = timezone.now()
    livro.dt_atualizacao = timezone.now()
    livro.save()
    print(f"Atualizado: {livro.titulo}")

class LivroCreateView(View):
    """View para criar um novo livro."""
    template_name = "adicionar_livro.html"

    def get(self, request):
        form = LivroCreateForm()
        editoras = tbl_editora.objects.all()
        return render(request, self.template_name, {"form": form, "editoras": editoras})


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
    # CORREÇÃO: Use os related names corretos do seu modelo
    livros = tbl_livro.objects.all().select_related('editora')
    
    # Para cada livro, busque autores e categorias
    livros_com_relacionados = []
    for livro in livros:
        # Busca autores através da tabela intermediária
        autores_ids = tbl_livro_autor.objects.filter(livro=livro).values_list('autor', flat=True)
        autores = tbl_autor.objects.filter(id_autor__in=autores_ids)
        
        # Busca categorias através da tabela intermediária
        categorias_ids = tbl_livro_categoria.objects.filter(livro=livro).values_list('categoria', flat=True)
        categorias = tbl_categoria.objects.filter(id_categoria__in=categorias_ids)
        
        livros_com_relacionados.append({
            'livro': livro,
            'autores': autores,
            'categorias': categorias
        })
    
    todas_categorias = tbl_categoria.objects.all()
    
    return render(request, 'tela_todos_os_livros.html', {
        'livros_com_relacionados': livros_com_relacionados,
        'categorias': todas_categorias
    })
    
# API para buscar um livro específico
@csrf_exempt
@require_http_methods(["GET"])
def api_livro_detail(request, livro_id):
    livro = get_object_or_404(tbl_livro, id_livro=livro_id)
    
    # Busca autores
    autores_ids = tbl_livro_autor.objects.filter(livro=livro).values_list('autor', flat=True)
    autores = list(tbl_autor.objects.filter(id_autor__in=autores_ids))
    
    # Busca categorias
    categorias_ids = tbl_livro_categoria.objects.filter(livro=livro).values_list('categoria', flat=True)
    categorias = list(tbl_categoria.objects.filter(id_categoria__in=categorias_ids))
    
    data = {
        'id': livro.id_livro,  # CORREÇÃO
        'titulo': livro.titulo,
        'ano_publicacao': livro.ano_publicacao,
        'editora': livro.editora.nome if livro.editora else '',
        'editora_id': livro.editora.id_editora if livro.editora else None,
        'autores': ', '.join([autor.nome for autor in autores]),
        'categoria': ', '.join([cat.nome for cat in categorias]) if categorias else '',
        'categoria_id': categorias.first().id_categoria if categorias else None,
        'status': livro.status,
        'data_criacao': livro.data_criacao.strftime('%d/%m/%Y') if livro.data_criacao else '',
        'data_atualizacao': livro.data_atualizacao.strftime('%d/%m/%Y') if livro.data_atualizacao else '',
    }
    
    return JsonResponse(data)

# API para atualizar um livro
@csrf_exempt
@require_http_methods(["PUT"])
def api_livro_update(request, livro_id):
    if request.method == 'PUT':
        try:
            livro = get_object_or_404(tbl_livro, id_livro=livro_id)
            data = json.loads(request.body)
            
            # Atualiza campos básicos
            livro.titulo = data.get('titulo', livro.titulo)
            livro.ano_publicacao = data.get('ano_publicacao', livro.ano_publicacao)
            livro.status = data.get('status', livro.status)
            
            # Atualiza relacionamentos (simplificado)
            if data.get('categoria_id'):
                try:
                    categoria = tbl_categoria.objects.get(id=data['categoria_id'])
                    
                    # Remove categorias antigas
                    tbl_livro_categoria.objects.filter(livro=livro).delete()
                    # Adiciona nova categoria
                    tbl_livro_categoria.objects.create(livro=livro, categoria=categoria)
                    
                except tbl_categoria.DoesNotExist:
                    pass
            
            # SALVA O LIVRO
            livro.save()
            
            return JsonResponse({'success': True, 'message': 'Livro atualizado com sucesso'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

# API para excluir um livro
@csrf_exempt
@require_http_methods(["DELETE"])
def api_livro_delete(request, livro_id):
    if request.method == 'DELETE':
        try:
            livro = get_object_or_404(tbl_livro, id_livro=livro_id)
            livro.delete()
            return JsonResponse({'success': True, 'message': 'Livro excluído com sucesso'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

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