"""Views para gerenciamento de livros."""
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views import View
import json
from ..forms import LivroCreateForm, LivroAutorForm, LivroCategoriaForm
from ..models import tbl_livro, tbl_livro_autor, tbl_livro_categoria, tbl_editora, tbl_autor, tbl_categoria, tbl_status_livro
from biblioteca.models import Emprestimo
from django.utils import timezone
from datetime import timedelta, date, datetime

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
            "livro_quantidade": livro.quantidade,
            "livro_capa": livro.capa.url if livro.capa else None
        })
    
def livro_list(request):
    livros = tbl_livro.objects.all().select_related(
        'editora', 'status'
    ).prefetch_related(
        'autores', 'categorias'
    ).order_by('-dt_criacao')
    
    # Calcular disponibilidade para cada livro
    livros_com_relacionados = []
    for livro in livros:
        # Contar empréstimos ativos
        emprestados_ativos = Emprestimo.objects.filter(
            livro=livro,
            dt_devolucao_real__isnull=True,
        ).count()
        
        # Calcular disponível (usando o máximo entre 0 e a diferença)
        # EVITAR VALORES NEGATIVOS
        disponivel_calculado = max(0, (livro.quantidade or 0) - emprestados_ativos)
        
        # Se o campo disponivel do model não está sendo atualizado, use o calculado
        # Ou atualize o campo no model:
        if livro.disponivel != disponivel_calculado:
            livro.disponivel = disponivel_calculado
            livro.save(update_fields=['disponivel'])
        
        livros_com_relacionados.append({
            'livro': livro,
            'autores': list(livro.autores.all()),
            'categorias': list(livro.categorias.all()),
            'disponivel_calculado': disponivel_calculado,  # Para debug
            'emprestados_ativos': emprestados_ativos,  # Para debug
            'isbn': livro.isbn if hasattr(livro, 'isbn') else "Não informado",
            'quantidade': livro.quantidade if hasattr(livro, 'quantidade') else 0,
            'disponivel': livro.disponivel if hasattr(livro, 'disponivel') else 0,
        })
    
    # DEBUG: Verifique os dados
    for item in livros_com_relacionados[:3]:  # Primeiros 3
        print(f"DEBUG Livro: {item['livro'].titulo}")
        print(f"  ISBN: {item['isbn']}")
        print(f"  Quantidade: {item['quantidade']}")
        print(f"  Disponível (campo): {item['disponivel']}")
        print(f"  Disponível (calculado): {item['disponivel_calculado']}")
        print(f"  Emprestados ativos: {item['emprestados_ativos']}")
    
    # Outros dados para o template
    editoras = tbl_editora.objects.all()
    categorias = tbl_categoria.objects.all()
    autores = tbl_autor.objects.all()
    status_list = tbl_status_livro.objects.filter(ativo=True)
    
    return render(request, 'livro/livro_list.html', {
        'livros_com_relacionados': livros_com_relacionados,
        'editoras': editoras,
        'categorias': categorias,
        'autores': autores,
        'status_list': status_list,
        'hoje': timezone.now().date(),
        'data_padrao': timezone.now().date() + timedelta(days=10)
    })
    
    # Outros dados para o template
    editoras = tbl_editora.objects.all()
    categorias = tbl_categoria.objects.all()
    autores = tbl_autor.objects.all()
    status_list = tbl_status_livro.objects.filter(ativo=True)
    
    return render(request, 'livro/livro_list.html', {
        'livros_com_relacionados': livros_com_relacionados,
        'editoras': editoras,
        'categorias': categorias,
        'autores': autores,
        'status_list': status_list,
        'hoje': timezone.now().date(),
        'data_padrao': timezone.now().date() + timedelta(days=10)
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
        categorias_ids = list(tbl_livro_categoria.objects.filter(livro=livro).values_list('categoria', flat=True))
        categorias = list(tbl_categoria.objects.filter(id_categoria__in=categorias_ids))
        categorias_nomes = ', '.join([cat.nome for cat in categorias]) if categorias else ''
        print(f"Categorias encontradas: {[c.nome for c in categorias]}")
        
        # Contar empréstimos ativos para cálculo correto
        emprestados_ativos = Emprestimo.objects.filter(
            livro=livro,
            dt_devolucao_real__isnull=True,
        ).count()
        
        # Calcular disponível corretamente
        quantidade = livro.quantidade if hasattr(livro, 'quantidade') else 0
        disponivel_calculado = max(0, quantidade - emprestados_ativos)
        
        # Processa categoria_id
        categoria_id = None
        if categorias:
            categoria_id = categorias[0].id_categoria
            print(f"Categoria ID selecionada: {categoria_id}")
            
        # Atualizar campo disponivel no banco se necessário
        if hasattr(livro, 'disponivel') and livro.disponivel != disponivel_calculado:
            livro.disponivel = disponivel_calculado
            livro.save(update_fields=['disponivel'])
        
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
            'categorias': categorias_nomes,
            'categorias_ids': categorias_ids,
            'status': livro.status.descricao if livro.status else '',
            'status_id': livro.status.id_status if livro.status else None,
            'isbn': livro.isbn if hasattr(livro, 'isbn') else "Não informado",
            'quantidade': quantidade,
            'disponivel': livro.disponivel if hasattr(livro, 'disponivel') else disponivel_calculado,
            'emprestados_ativos': emprestados_ativos,
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
@require_http_methods(["PUT", "POST"])
def api_livro_update(request, livro_id):
    if request.method == 'POST' or request.method == 'PUT':
        try:
            livro = get_object_or_404(tbl_livro, id_livro=livro_id)
            
            data = {}
            files = {}

            if request.content_type.startswith('multipart/form-data'):
                # Se veio do FormData (com ou sem imagem)
                data = request.POST.dict() # Converte para dicionário Python normal
                files = request.FILES
            else:
                # Se veio JSON puro
                try:
                    data = json.loads(request.body)
                except:
                    data = {}

            print(f"DEBUG: Dados processados: {data}")
            
            # DEBUG DETALHADO DO STATUS
            print(f"DEBUG: Status atual do livro: {livro.status.descricao if livro.status else 'None'}")
            print(f"DEBUG: status_id recebido: {data.get('status_id')}")
            
            if 'status_id' in data and data['status_id']:
                try:
                    status_obj = tbl_status_livro.objects.get(id_status=data['status_id'])
                    
                    livro.status = status_obj
                    print(f"DEBUG: Status atualizado para: {status_obj.descricao}")
                except tbl_status_livro.DoesNotExist:
                    print(f"DEBUG: Status ID {data['status_id']} não encontrado")
            else:
                print("DEBUG: Nenhum status_id fornecido nos dados")
            
            if 'titulo' in data:
                livro.titulo = data['titulo']
            
            if 'ano_publicacao' in data:
                livro.ano_publicacao = data['ano_publicacao']
                
            # Tratamento especial para quantidade (int)
            if 'quantidade' in data:
                qtde = data['quantidade']
                if qtde is not None and qtde != '':
                    try:
                        nova_quantidade = int(qtde)
                        quantidade_original = livro.quantidade
                        
                        print(f"DEBUG: Atualizando quantidade de {quantidade_original} para {nova_quantidade}")
                        
                        # 1. Conta empréstimos ativos ANTES de mudar qualquer coisa
                        emprestimos_ativos = livro.emprestimos.filter(status='ativo').count()
                        print(f"DEBUG: Empréstimos ativos: {emprestimos_ativos}")
                        
                        # 2. Atualiza a quantidade (estoque total)
                        livro.quantidade = nova_quantidade
                        
                        # 3. Calcula o novo disponivel CORRETAMENTE
                        # disponivel = quantidade - emprestimos_ativos
                        novo_disponivel = max(0, nova_quantidade - emprestimos_ativos)
                        
                        print(f"DEBUG: Cálculo: {nova_quantidade} - {emprestimos_ativos} = {novo_disponivel}")
                        
                        # 4. Atualiza o disponivel
                        livro.disponivel = novo_disponivel
                        
                        print(f"DEBUG: Disponível ajustado para: {livro.disponivel}")
                        
                    except (ValueError, TypeError) as e:
                        print(f"DEBUG: Erro ao converter quantidade: {e}")
                        return JsonResponse({
                            'success': False, 
                            'error': 'Quantidade deve ser um número válido'
                        }, status=400)

            # Atualiza Editora
            if 'editora_id' in data and data['editora_id']:
                try:
                    livro.editora = tbl_editora.objects.get(id_editora=data['editora_id'])
                except tbl_editora.DoesNotExist:
                    return JsonResponse({'success': False, 'error': 'Editora inválida'}, status=404)

            if 'capa' in files:
                print("DEBUG: Salvando nova capa...")
                livro.capa = files['capa']
            elif data.get('remove_capa') == 'true':
                print("DEBUG: Removendo capa...")
                if livro.capa:
                    livro.capa.delete(save=False)
                livro.capa = None

            # 4. SALVA O LIVRO (Básico + Capa)
            livro.save()
            print(f"Livro {livro_id} salvo com sucesso.")

            if not data.get('status_id'):  # Se status não foi definido manualmente
                if livro.disponivel > 0:
                    try:
                        status_disponivel = tbl_status_livro.objects.get(descricao='Disponível')
                        livro.status = status_disponivel
                        livro.save()
                        print(f"DEBUG: Status auto-atualizado para 'Disponível' (disponivel={livro.disponivel})")
                    except tbl_status_livro.DoesNotExist:
                        print("DEBUG: Status 'Disponível' não encontrado")
                else:
                    try:
                        status_indisponivel = tbl_status_livro.objects.get(descricao='Indisponível')
                        livro.status = status_indisponivel
                        livro.save()
                        print(f"DEBUG: Status auto-atualizado para 'Indisponível' (disponivel={livro.disponivel})")
                    except tbl_status_livro.DoesNotExist:
                        print("DEBUG: Status 'Indisponível' não encontrado")

            # 5. ATUALIZAÇÃO MANY-TO-MANY (Autores e Categorias)
            # Função auxiliar para não repetir código
            def atualizar_relacao(campo_ids, model_relacao, model_destino, campo_destino_str):
                # Tenta pegar a lista de IDs
                ids_raw = data.get(campo_ids)
                
                # Se veio do FormData, pode vir como string "[1, 2]"
                if isinstance(ids_raw, str):
                    try:
                        ids_list = json.loads(ids_raw)
                    except:
                        # Se não for JSON, pode ser um ID único string "1"
                        ids_list = [int(ids_raw)] if ids_raw.isdigit() else []
                # Se veio do JSON puro, já é lista [1, 2]
                elif isinstance(ids_raw, list):
                    ids_list = ids_raw
                else:
                    ids_list = []

                if ids_list is not None:
                    # Limpa relações antigas
                    model_relacao.objects.filter(livro=livro).delete()
                    
                    # Cria novas
                    for obj_id in ids_list:
                        try:
                            # Monta o filtro dinâmico (id_autor=1 ou id_categoria=1)
                            kwargs_get = {f'id_{campo_destino_str}': obj_id}
                            obj_destino = model_destino.objects.get(**kwargs_get)
                            
                            # Monta a criação dinâmica
                            kwargs_create = {'livro': livro, campo_destino_str: obj_destino}
                            model_relacao.objects.create(**kwargs_create)
                        except Exception as e:
                            print(f"Erro ao vincular {campo_destino_str} {obj_id}: {e}")

            # Executa para Autores
            atualizar_relacao('autores_ids', tbl_livro_autor, tbl_autor, 'autor')
            
            # Executa para Categorias
            atualizar_relacao('categorias_ids', tbl_livro_categoria, tbl_categoria, 'categoria')

            return JsonResponse({
                'success': True, 
                'message': 'Livro atualizado!',
                'livro': {
                    'quantidade': livro.quantidade,
                    'disponivel': livro.disponivel,
                    'status': livro.status.descricao if livro.status else None,
                    'emprestimos_ativos': livro.emprestimos.filter(status='ativo').count()
                }
            })

        except Exception as e:
            print(f"ERRO CRÍTICO: {str(e)}")
            import traceback
            traceback.print_exc()
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'error': 'Método inválido'}, status=405)

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
    livros_sem_data = tbl_livro.objects.filter(dt_criacao__isnull=True)
    count = 0
    
    for livro in livros_sem_data:
        livro.dt_criacao = timezone.now()
        livro.dt_atualizacao = timezone.now()
        livro.save()
        count += 1
    
    return HttpResponse(f"{count} livros atualizados com datas.")