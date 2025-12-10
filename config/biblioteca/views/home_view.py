# views/home_views.py
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from ..models import (  
    tbl_livro, tbl_editora, tbl_categoria, 
    tbl_autor, tbl_status_livro, Emprestimo
)

def listar_livros(request):
    query = request.GET.get('q', '')
    
    # Query base
    livros_list = tbl_livro.objects.all().select_related(
        'editora', 'status'
    ).prefetch_related(
        'autores', 'categorias'
    ).order_by('-dt_criacao')
    
    # Aplicar filtro de busca
    if query:
        livros_list = livros_list.filter(
            Q(titulo__icontains=query) |
            Q(autores__nome__icontains=query) |
            Q(categorias__nome__icontains=query) |
            Q(isbn__icontains=query)
        ).distinct()
    
    # Paginação
    paginator = Paginator(livros_list, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Calcular disponibilidade para cada livro
    livros_com_disponibilidade = []
    for livro in page_obj:
        emprestados_ativos = Emprestimo.objects.filter(
            livro=livro,
        ).count()
        
        # Calcular disponível
        disponivel = (livro.quantidade or 0) - emprestados_ativos
        esta_disponivel = disponivel > 0
        
        livros_com_disponibilidade.append({
            'livro': livro,
            'disponivel': esta_disponivel,
            'quantidade_disponivel': max(0, disponivel),
            'autores_str': ', '.join([a.nome for a in livro.autores.all()]),
            'categorias_str': ', '.join([c.nome for c in livro.categorias.all()]),
        })
    
    context = {
        'livros_com_relacionados': livros_com_disponibilidade,
        'page_obj': page_obj,
        'query': query,
        'categorias': tbl_categoria.objects.all(),
        'status_options': tbl_status_livro.objects.filter(ativo=True),
        'autores': tbl_autor.objects.all(),
        'editoras': tbl_editora.objects.all(),
        'hoje': timezone.now().date(),
        'data_padrao': timezone.now().date() + timedelta(days=10)
    }
    
    return render(request, 'dashboard/home.html', context)

def livro_dados_json(request, livro_id):
    """Retorna dados do livro em JSON para o modal"""
    try:
        livro = get_object_or_404(
            tbl_livro.objects.select_related('editora', 'status')
                            .prefetch_related('autores', 'categorias'), 
            id_livro=livro_id
        )
        
        # Calcular disponibilidade - AJUSTE CONFORME SEU MODEL
        emprestados_ativos = Emprestimo.objects.filter(
            livro=livro,
            # Ajuste este filtro
            # devolvido=False  # ou status='emprestado'
        ).count()
        
        disponivel = (livro.quantidade or 0) - emprestados_ativos
        esta_disponivel = disponivel > 0
        
        # URL da capa
        capa_url = ''
        if livro.capa and hasattr(livro.capa, 'url'):
            capa_url = request.build_absolute_uri(livro.capa.url)
        else:
            capa_url = '/static/img/placeholder.png'
        
        data = {
            'id_livro': livro.id_livro,
            'titulo': livro.titulo,
            'autores': ', '.join([a.nome for a in livro.autores.all()]),
            'categorias': ', '.join([c.nome for c in livro.categorias.all()]),
            'editora': livro.editora.nome if livro.editora else 'Não informado',
            'isbn': livro.isbn or 'Não informado',
            'descricao': livro.descricao or 'Sem descrição disponível.',
            'quantidade_total': livro.quantidade or 0,
            'quantidade_disponivel': max(0, disponivel),
            'disponivel': esta_disponivel,
            'ano_publicacao': livro.ano_publicacao or 'Não informado',
            'status': livro.status.nome if livro.status else 'Indefinido',
            'capa_url': capa_url,
            'user_authenticated': request.user.is_authenticated,
            'dt_criacao': livro.dt_criacao.strftime('%d/%m/%Y') if livro.dt_criacao else '',
            'sinopse': livro.sinopse or livro.descricao or 'Sem sinopse disponível.',
            'success': True
        }
        
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'message': 'Erro ao buscar dados do livro'
        }, status=500)