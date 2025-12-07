"""Views para gerenciamento de livros."""
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views import View
import json
from ..forms import LivroCreateForm, LivroAutorForm, LivroCategoriaForm
from ..models import tbl_livro, tbl_livro_autor, tbl_livro_categoria, tbl_editora, tbl_autor, tbl_categoria, tbl_status_livro


class LivroCreateView(View):
    template_name = "livro/livro_form.html"

    def get(self, request):
        return render(request, self.template_name, {
            "form": LivroCreateForm(),
            "editoras": tbl_editora.objects.all(),
            "status_list": tbl_status_livro.objects.filter(ativo=True)
        })

    def post(self, request):
        print("DEBUG: POST recebido")

        form = LivroCreateForm(request.POST, request.FILES)
        editoras = tbl_editora.objects.all()
        status_list = tbl_status_livro.objects.filter(ativo=True)

        if not form.is_valid():
            print("DEBUG: Form inválido:", form.errors)
            return render(request, self.template_name, {
                "form": form,
                "editoras": editoras,
                "status_list": status_list
            })

        # FORM
        livro = form.save()

        return render(request, self.template_name, {
            "form": LivroCreateForm(),
            "editoras": editoras,
            "status_list": status_list,
            "sucesso": True,
            "livro_id": livro.id_livro,
            "livro_nome": livro.titulo,
            "livro_capa": livro.capa.url if livro.capa else None
        })


def livro_list(request):
    """Exibe uma lista de todos os livros disponíveis na biblioteca."""
    livros = tbl_livro.objects.all().select_related('editora', 'status')
    
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
    todas_editoras = tbl_editora.objects.all()
    todos_autores = tbl_autor.objects.all()
    
    return render(request, 'livro/livro_list.html', {
        'livros_com_relacionados': livros_com_relacionados,
        'categorias': todas_categorias,
        'editoras': todas_editoras,
        'autores': todos_autores,
        "status_list": tbl_status_livro.objects.filter(ativo=True)
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
        
        # Busca autores
        autores_ids = list(tbl_livro_autor.objects.filter(livro=livro).values_list('autor', flat=True))
        autores = list(tbl_autor.objects.filter(id_autor__in=autores_ids))
        autores_nomes = ', '.join([autor.nome for autor in autores])
        print(f"Autores encontrados: {[a.nome for a in autores]}")
        print(f"IDs dos autores: {autores_ids}")
        
        # Busca categorias
        categorias_ids = tbl_livro_categoria.objects.filter(livro=livro).values_list('categoria', flat=True)
        categorias = list(tbl_categoria.objects.filter(id_categoria__in=categorias_ids))
        categorias_nomes = ', '.join([cat.nome for cat in categorias]) if categorias else ''
        print(f"Categorias encontradas: {[c.nome for c in categorias]}")
        
        # Processa categoria_id
        categoria_id = None
        if categorias:
            categoria_id = categorias[0].id_categoria
            print(f"Categoria ID selecionada: {categoria_id}")
        
        # Processa status
        status_id = None
        status_value = ''
        
        if livro.status and hasattr(livro.status, 'id_status'):
            status_id = livro.status.id_status
            status_value = livro.status.descricao
            print(f"Status: {status_value} (ID: {status_id})")
        
        # Preparar dados
        data = {
            'id': livro.id_livro,
            'titulo': livro.titulo,
            'ano_publicacao': livro.ano_publicacao,
            'editora': livro.editora.nome if livro.editora else '',
            'editora_id': livro.editora.id_editora if livro.editora else None,
            'autores': autores_nomes,  # String com nomes
            'autores_ids': autores_ids,  # Array de IDs para o Select2 (IMPORTANTE!)
            'categoria': categorias_nomes,
            'categoria_id': categoria_id,
            'status': status_value,
            'status_id': status_id
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
        
        # Adicionar capa se existir
        if livro.capa:
            data['capa_url'] = livro.capa.url
            data['tem_capa'] = True
        else:
            data['tem_capa'] = False
        
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
            livro = get_object_or_404(tbl_livro, id_livro=livro_id)
            
            # Verifica se é multipart/form-data (com arquivo)
            if request.content_type.startswith('multipart/form-data'):
                print("DEBUG: Recebendo dados multipart/form-data")
                print(f"POST data: {dict(request.POST)}")
                print(f"FILES data: {dict(request.FILES)}")
                
                # Processa campos do formulário
                titulo = request.POST.get('titulo')
                ano_publicacao = request.POST.get('ano_publicacao')
                editora_id = request.POST.get('editora_id')
                categoria_id = request.POST.get('categoria_id')
                status_id = request.POST.get('status_id')
                autores_ids_json = request.POST.get('autores_ids')
                remove_capa = request.POST.get('remove_capa') == 'true'
                
                # Atualiza campos básicos
                if titulo:
                    livro.titulo = titulo
                if ano_publicacao:
                    livro.ano_publicacao = ano_publicacao
                
                # Atualiza status
                if status_id:
                    try:
                        status_obj = tbl_status_livro.objects.get(id_status=status_id)
                        livro.status = status_obj
                        print(f"Status atualizado para: {status_obj.descricao} (ID: {status_obj.id_status})")
                    except tbl_status_livro.DoesNotExist:
                        return JsonResponse({
                            'success': False, 
                            'error': 'Status não encontrado'
                        }, status=404)
                
                # Atualiza editora
                if editora_id:
                    try:
                        editora = tbl_editora.objects.get(id_editora=editora_id)
                        livro.editora = editora
                    except tbl_editora.DoesNotExist:
                        return JsonResponse({
                            'success': False, 
                            'error': 'Editora não encontrada'
                        }, status=404)
                
                # Processa a capa
                if 'capa' in request.FILES:
                    print("DEBUG: Nova capa recebida")
                    livro.capa = request.FILES['capa']
                elif remove_capa and livro.capa:
                    print("DEBUG: Removendo capa atual")
                    livro.capa.delete(save=False)  # Remove o arquivo
                    livro.capa = None  # Limpa o campo
                
                # Salva o livro (isso salva a imagem também)
                livro.save()
                print(f"Livro {livro_id} salvo.")
                
                # Processa autores
                if autores_ids_json:
                    try:
                        autores_ids = json.loads(autores_ids_json)
                        print(f"DEBUG: Autores recebidos: {autores_ids}")
                        
                        # Remove autores existentes
                        tbl_livro_autor.objects.filter(livro=livro).delete()
                        
                        # Adiciona novos autores
                        if autores_ids and len(autores_ids) > 0:
                            for autor_id in autores_ids:
                                try:
                                    autor = tbl_autor.objects.get(id_autor=autor_id)
                                    tbl_livro_autor.objects.create(livro=livro, autor=autor)
                                    print(f"Autor adicionado: {autor.nome} (ID: {autor_id})")
                                except tbl_autor.DoesNotExist:
                                    print(f"Autor ID {autor_id} não encontrado, pulando...")
                    except json.JSONDecodeError as e:
                        print(f"Erro ao decodificar autores_ids: {e}")
                
                # Atualiza categorias
                if categoria_id:
                    try:
                        categoria = tbl_categoria.objects.get(id_categoria=categoria_id)
                        # Remove categorias existentes
                        tbl_livro_categoria.objects.filter(livro=livro).delete()
                        # Adiciona nova categoria
                        tbl_livro_categoria.objects.create(livro=livro, categoria=categoria)
                    except tbl_categoria.DoesNotExist:
                        return JsonResponse({
                            'success': False, 
                            'error': 'Categoria não encontrada'
                        }, status=404)
                
            else:
                # Processa JSON (modo antigo para compatibilidade)
                data = json.loads(request.body)
                print(f"Dados recebidos para atualização (JSON): {data}")
                
                # Atualiza campos básicos
                if 'titulo' in data:
                    livro.titulo = data['titulo']
                if 'ano_publicacao' in data:
                    livro.ano_publicacao = data['ano_publicacao']
                if 'status_id' in data:
                    try:
                        status_obj = tbl_status_livro.objects.get(id_status=data['status_id'])
                        livro.status = status_obj
                        print(f"Status atualizado para: {status_obj.descricao} (ID: {status_obj.id_status})")
                    except tbl_status_livro.DoesNotExist:
                        return JsonResponse({
                            'success': False, 
                            'error': 'Status não encontrado'
                        }, status=404)
                
                # Atualiza editora
                if 'editora_id' in data and data['editora_id']:
                    try:
                        editora = tbl_editora.objects.get(id_editora=data['editora_id'])
                        livro.editora = editora
                    except tbl_editora.DoesNotExist:
                        return JsonResponse({
                            'success': False, 
                            'error': 'Editora não encontrada'
                        }, status=404)
                
                # Salva o livro
                livro.save()
                print(f"Livro {livro_id} salvo.")
                
                # Atualiza autores
                if 'autores_ids' in data:
                    print(f"Atualizando autores: {data['autores_ids']}")
                    # Remove autores existentes
                    tbl_livro_autor.objects.filter(livro=livro).delete()
                    # Adiciona novos autores
                    if data['autores_ids'] and len(data['autores_ids']) > 0:
                        for autor_id in data['autores_ids']:
                            try:
                                autor = tbl_autor.objects.get(id_autor=autor_id)
                                tbl_livro_autor.objects.create(livro=livro, autor=autor)
                                print(f"Autor adicionado: {autor.nome} (ID: {autor_id})")
                            except tbl_autor.DoesNotExist:
                                print(f"Autor ID {autor_id} não encontrado, pulando...")
                
                # Atualiza categorias
                if 'categoria_id' in data and data['categoria_id']:
                    try:
                        categoria = tbl_categoria.objects.get(id_categoria=data['categoria_id'])
                        # Remove categorias existentes
                        tbl_livro_categoria.objects.filter(livro=livro).delete()
                        # Adiciona nova categoria
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
            print(f"Erro na atualização: {str(e)}")
            import traceback
            traceback.print_exc()
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
        return redirect('livro_list')


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