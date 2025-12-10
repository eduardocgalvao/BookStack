// static/js/livro/home.js

let currentBookData = null;

function openBookModal(bookId) {
    console.log('Abrindo modal para livro ID:', bookId);
    
    // Mostrar modal imediatamente com loading
    const modal = document.getElementById('bookModal');
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
    
    // Limpar dados anteriores
    document.getElementById('modalBookTitle').textContent = 'Carregando...';
    // document.getElementById('modalBookCover').src = '';
    document.getElementById('modalBookDescription').textContent = '';
    
    // Fazer requisição para dados do livro
    fetch(`/dashboard/dados-livro/${bookId}/`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Dados recebidos:', data);
            currentBookData = data;
            populateModal(data);
        })
        .catch(error => {
            console.error('Erro ao buscar dados do livro:', error);
            
            // Mostrar mensagem de erro no modal
            document.getElementById('modalBookTitle').textContent = 'Erro';
            document.getElementById('modalBookDescription').textContent = 
                'Não foi possível carregar os detalhes do livro. Por favor, tente novamente.';
            
            // Desabilitar botão de empréstimo
            const btnEmprestar = document.getElementById('btnEmprestar');
            if (btnEmprestar) {
                btnEmprestar.disabled = true;
                btnEmprestar.textContent = 'Erro ao carregar';
            }
        });
}

function populateModal(data) {
    // Preencher todos os campos
    const fields = {
        'modalBookTitle': data.titulo,
        'modalBookTitleText': data.titulo,
        'modalBookAuthors': data.autores || 'Não informado',
        'modalBookPublisher': data.editora || 'Não informado',
        'modalBookCategories': data.categorias || 'Não informado',
        'modalBookISBN': data.isbn || 'Não informado',
        'modalBookYear': data.ano_publicacao || 'Não informado',
        'modalBookQuantity': `${data.quantidade_total || 0} unidade(s) total`,
        'modalBookAvailable': `${data.quantidade_disponivel || 0} unidade(s) disponível(eis)`,
        'modalBookStatus': data.status || 'Indefinido',
        'modalBookCreated': data.dt_criacao || 'Não informado',
        'modalBookDescription': data.descricao || data.sinopse || 'Sem descrição disponível.'
    };
    
    // Atualizar cada campo
    Object.keys(fields).forEach(fieldId => {
        const element = document.getElementById(fieldId);
        if (element) {
            element.textContent = fields[fieldId];
        }
    });
    
    // Atualizar capa
    const coverImg = document.getElementById('modalBookCover');
    if (coverImg && data.capa_url) {
        coverImg.src = data.capa_url;
        coverImg.alt = `Capa do livro: ${data.titulo}`;
    } else if (coverImg) {
        coverImg.src = '/static/img/placeholder.png';
        coverImg.alt = 'Capa não disponível';
    }
    
    // Configurar botão de empréstimo
    const btnEmprestar = document.getElementById('btnEmprestar');
    if (btnEmprestar) {
        if (data.disponivel && data.user_authenticated) {
            btnEmprestar.disabled = false;
            btnEmprestar.innerHTML = '📥 Emprestar Livro';
            btnEmprestar.onclick = () => goToLoan(data.id_livro);
        } else {
            btnEmprestar.disabled = true;
            if (!data.user_authenticated) {
                btnEmprestar.innerHTML = '🔑 Faça login para emprestar';
                // Permitir clique para login mesmo desabilitado
                btnEmprestar.disabled = false;
                btnEmprestar.onclick = () => {
                    window.location.href = `/login/?next=${window.location.pathname}`;
                };
            } else if (!data.disponivel) {
                btnEmprestar.innerHTML = '📕 Indisponível para empréstimo';
            }
        }
    }
}

function closeModal(event) {
    if (event) {
        event.stopPropagation();
    }
    
    const modal = document.getElementById('bookModal');
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
    currentBookData = null;
}

function goToLoan(bookId) {
    if (currentBookData && currentBookData.disponivel) {
        // Ajuste esta URL conforme sua configuração
        window.location.href = `/emprestimo/novo/?livro=${bookId}`;
    }
}

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    // Fechar modal com ESC
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            closeModal();
        }
    });
    
    // Fechar modal ao clicar fora
    document.addEventListener('click', function(event) {
        const modal = document.getElementById('bookModal');
        if (modal && modal.style.display === 'flex' && event.target === modal) {
            closeModal();
        }
    });
    
    // Adicionar indicador de clique nos cards
    const cards = document.querySelectorAll('.book-card');
    cards.forEach(card => {
        // Adicionar efeito visual de clique
        card.style.cursor = 'pointer';
        card.title = 'Clique para ver detalhes';
    });
    
    console.log('Sistema de livros carregado. Cards prontos:', cards.length);
});