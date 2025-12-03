"""Views para gerenciamento de livros."""
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views import View
import json
from ..forms import LivroCreateForm, LivroAutorForm, LivroCategoriaForm
from ..models import tbl_livro, tbl_livro_autor, tbl_livro_categoria, tbl_editora, tbl_autor, tbl_categoria


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
    livros = tbl_livro.objects.all().select_related('editora')
    
    livros_com_relacionados = []
    for livro in livros:
        # Busca autores
        autores_ids = tbl_livro_autor.objects.filter(livro=livro).values_list('autor', flat=True)
        autores = tbl_autor.objects.filter(id_autor__in=autores_ids)
        
        # Busca categorias
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


@csrf_exempt
@require_http_methods(["GET"])
def api_livro_detail(request, livro_id):
    """API para buscar detalhes de um livro específico."""
    try:
        print(f"=== DEBUG: Buscando livro ID: {livro_id} ===")
        
        livro = get_object_or_404(tbl_livro, id_livro=livro_id)
        print(f"Livro encontrado: {livro.titulo} (ID: {livro.id_livro})")
        
        # DEBUG: Verificar campos do livro
        print(f"Campos do livro: {[f.name for f in livro._meta.fields]}")
        print(f"dt_criacao existe? {hasattr(livro, 'dt_criacao')}")
        if hasattr(livro, 'dt_criacao'):
            print(f"dt_criacao valor: {livro.dt_criacao}")
        
        # Busca autores
        autores_ids = tbl_livro_autor.objects.filter(livro=livro).values_list('autor', flat=True)
        autores = list(tbl_autor.objects.filter(id_autor__in=autores_ids))
        print(f"Autores encontrados: {[a.nome for a in autores]}")
        
        # Busca categorias
        categorias_ids = tbl_livro_categoria.objects.filter(livro=livro).values_list('categoria', flat=True)
        categorias = list(tbl_categoria.objects.filter(id_categoria__in=categorias_ids))
        print(f"Categorias encontradas: {[c.nome for c in categorias]}")
        
        # Processa categoria_id
        categoria_id = None
        if categorias:
            categoria_id = categorias[0].id_categoria
            print(f"Categoria ID selecionada: {categoria_id}")
        
        status_value = ''
        if hasattr(livro, 'status'):
            if hasattr(livro.status, 'descricao'):  # Se for objeto com campo descricao
                status_value = livro.status.descricao
            elif hasattr(livro.status, 'nome'):  # Se for objeto com campo nome
                status_value = livro.status.nome
            elif hasattr(livro.status, 'status'):  # Se for objeto com campo status
                status_value = livro.status.status
            else:
                status_value = str(livro.status)
        
        print(f"Status valor: {status_value}")
        
        # Preparar dados
        data = {
            'id': livro.id_livro,
            'titulo': livro.titulo,
            'ano_publicacao': livro.ano_publicacao,
            'editora': livro.editora.nome if livro.editora else '',
            'editora_id': livro.editora.id_editora if livro.editora else None,
            'autores': ', '.join([autor.nome for autor in autores]),
            'categoria': ', '.join([cat.nome for cat in categorias]) if categorias else '',
            'categoria_id': categoria_id,
            'status': status_value,
        }
        
        # Adicionar datas com verificação segura
        if hasattr(livro, 'dt_criacao') and livro.dt_criacao:
            try:
                data['dt_criacao'] = livro.dt_criacao.strftime('%d/%m/%Y')
            except Exception as e:
                print(f"Erro ao formatar dt_criacao: {e}")
                data['dt_criacao'] = ''
        else:
            data['dt_criacao'] = ''
        
        if hasattr(livro, 'dt_atualizacao') and livro.dt_atualizacao:
            try:
                data['dt_atualizacao'] = livro.dt_atualizacao.strftime('%d/%m/%Y')
            except Exception as e:
                print(f"Erro ao formatar dt_atualizacao: {e}")
                data['dt_atualizacao'] = ''
        else:
            data['dt_atualizacao'] = ''
        
        print(f"Dados preparados: {data}")
        return JsonResponse(data)
    
    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        print(f"=== ERRO DETALHADO ===")
        print(error_traceback)
        print(f"=== FIM ERRO ===")
        
        return JsonResponse({
            'error': str(e),
            'traceback': error_traceback,
            'success': False
        }, status=500)


@csrf_exempt
@require_http_methods(["PUT"])
def api_livro_update(request, livro_id):
    """API para atualizar um livro."""
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            livro = get_object_or_404(tbl_livro, id_livro=livro_id)
            
            # Atualiza campos básicos
            if 'titulo' in data:
                livro.titulo = data['titulo']
            if 'ano_publicacao' in data:
                livro.ano_publicacao = data['ano_publicacao']
            if 'status' in data:
                status_value = data['status']
            if hasattr(livro, 'status') and not hasattr(livro.status, 'descricao'):
                livro.status = status_value
            
            # Atualiza editora se for enviado editora_id
            if 'editora_id' in data and data['editora_id']:
                try:
                    editora = tbl_editora.objects.get(id_editora=data['editora_id'])
                    livro.editora = editora
                except tbl_editora.DoesNotExist:
                    return JsonResponse({
                        'success': False, 
                        'error': 'Editora não encontrada'
                    }, status=404)
            
            # Salva para atualizar dt_atualizacao
            livro.save()
            
            # Atualiza categorias - CORREÇÃO: Use id_categoria em vez de id
            if 'categoria_id' in data and data['categoria_id']:
                try:
                    categoria = tbl_categoria.objects.get(id_categoria=data['categoria_id'])
                    # Remove todas as categorias existentes
                    tbl_livro_categoria.objects.filter(livro=livro).delete()
                    # Adiciona a nova categoria
                    tbl_livro_categoria.objects.create(livro=livro, categoria=categoria)
                except tbl_categoria.DoesNotExist:
                    return JsonResponse({
                        'success': False, 
                        'error': 'Categoria não encontrada'
                    }, status=404)
            
            return JsonResponse({
                'success': True, 
                'message': 'Livro atualizado com sucesso'
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False, 
                'error': 'JSON inválido'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False, 
                'error': str(e)
            }, status=500)


@csrf_exempt
@require_http_methods(["DELETE"])
def api_livro_delete(request, livro_id):
    """API para excluir um livro."""
    if request.method == 'DELETE':
        try:
            livro = get_object_or_404(tbl_livro, id_livro=livro_id)
            livro_titulo = livro.titulo
            livro.delete()
            
            return JsonResponse({
                'success': True, 
                'message': f'Livro "{livro_titulo}" excluído com sucesso'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False, 
                'error': str(e)
            }, status=500)


class RemoverLivroView(View):
    """View para remover um livro."""
    def post(self, request, pk):
        livro = get_object_or_404(tbl_livro, id_livro=pk)
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


# VIEW ADICIONAL PARA POPULAR DATAS FALTANTES
def popular_datas_livros(request):
    """View para popular datas de criação/atualização para livros que não tem."""
    from django.utils import timezone
    from django.http import HttpResponse
    
    livros_sem_data = tbl_livro.objects.filter(dt_criacao__isnull=True)
    count = 0
    
    for livro in livros_sem_data:
        livro.dt_criacao = timezone.now()
        livro.dt_atualizacao = timezone.now()
        livro.save()
        count += 1
    
    return HttpResponse(f"{count} livros atualizados com datas.")