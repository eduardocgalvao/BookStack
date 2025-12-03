// todos_livros.js - Script atualizado
console.log("Script todos_livros.js carregado");

// Configuração do CSRF para AJAX
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

console.log("API_URLS:", window.API_URLS);
console.log("CSRF Token:", csrftoken ? "Encontrado" : "Não encontrado");

// Funções AJAX
async function fetchLivro(id) {
    console.log(`Buscando livro ID: ${id}`);
    try {
        const url = `/api/livro/${id}/`;
        console.log("URL:", url);
        
        const response = await fetch(url, {
            headers: {
                'X-CSRFToken': csrftoken,
                'Accept': 'application/json'
            }
        });
        
        console.log("Status:", response.status);
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error(`Erro HTTP ${response.status}:`, errorText);
            throw new Error(`Erro ${response.status}: Não foi possível carregar o livro`);
        }
        
        const data = await response.json();
        console.log("Dados recebidos:", data);
        return data;
        
    } catch (error) {
        console.error('Erro ao buscar livro:', error);
        alert('Erro ao carregar dados do livro: ' + error.message);
        return null;
    }
}

async function updateLivro(id, data) {
    console.log(`Atualizando livro ID: ${id}`, data);
    try {
        const url = `/api/livro/${id}/update/`;
        console.log("URL:", url);
        
        const response = await fetch(url, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
                'Accept': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        console.log("Status:", response.status);
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error(`Erro HTTP ${response.status}:`, errorText);
            throw new Error(`Erro ${response.status}: Não foi possível atualizar o livro`);
        }
        
        return await response.json();
        
    } catch (error) {
        console.error('Erro ao atualizar livro:', error);
        return { 
            success: false, 
            error: error.message || 'Erro desconhecido ao atualizar' 
        };
    }
}

async function deleteLivro(id) {
    console.log(`Excluindo livro ID: ${id}`);
    try {
        const url = `/api/livro/${id}/delete/`;
        console.log("URL:", url);
        
        const response = await fetch(url, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrftoken,
                'Accept': 'application/json'
            }
        });
        
        console.log("Status:", response.status);
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error(`Erro HTTP ${response.status}:`, errorText);
            throw new Error(`Erro ${response.status}: Não foi possível excluir o livro`);
        }
        
        return await response.json();
        
    } catch (error) {
        console.error('Erro ao excluir livro:', error);
        return { 
            success: false, 
            error: error.message || 'Erro desconhecido ao excluir' 
        };
    }
}

// Variáveis para controle
let livroParaExcluir = null;
let livroParaEditar = null;
let autoresSelect2Instance = null;

// Configuração dos eventos quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM carregado, configurando eventos...");
    
    // ========== FUNÇÃO: INICIALIZAR SELECT2 PARA AUTORES ==========
    function inicializarSelect2Autores() {
        if (!autoresSelect2Instance && $('#edit-autores').length) {
            autoresSelect2Instance = $('#edit-autores').select2({
                width: '100%',
                placeholder: 'Selecione os autores',
                allowClear: true,
                dropdownParent: $('#edit-modal')
            });
            console.log("Select2 inicializado para autores");
        }
    }
    
    // ========== FUNÇÃO: LIMPAR SELECT2 QUANDO MODAL FECHAR ==========
    function limparSelect2Autores() {
        if (autoresSelect2Instance) {
            autoresSelect2Instance.val(null).trigger('change');
        }
    }
    
    // ========== EVENTO: ABRIR MODAL DE EDIÇÃO ==========
    const editIcons = document.querySelectorAll(".edit-icon");
    console.log(`Encontrados ${editIcons.length} ícones de edição`);
    
    editIcons.forEach((icon) => {
        icon.addEventListener("click", async function() {
            const livroId = this.getAttribute("data-id");
            console.log(`Clicou em editar livro ID: ${livroId}`);
            
            // Busca dados do livro
            const livro = await fetchLivro(livroId);
            if (livro) {
                console.log("Dados do livro para edição:", livro);
                
                // Preenche o formulário
                document.getElementById("edit-id").value = livro.id;
                document.getElementById("edit-titulo").value = livro.titulo || '';
                document.getElementById("edit-editora").value = livro.editora_id || '';
                document.getElementById("edit-ano").value = livro.ano_publicacao || '';
                document.getElementById("edit-categoria").value = livro.categoria_id || '';
                document.getElementById("edit-status").value = livro.status_id || '';
                
                // Inicializa Select2 se ainda não foi
                inicializarSelect2Autores();
                
                // Preenche os autores no Select2 usando os IDs
                // AGORA usando 'autores_ids' (plural)
                if (livro.autores_ids && Array.isArray(livro.autores_ids)) {
                    $('#edit-autores').val(livro.autores_ids).trigger('change');
                    console.log("Autores preenchidos:", livro.autores_ids);
                } else {
                    console.log("Nenhum autor encontrado ou formato inválido");
                    $('#edit-autores').val(null).trigger('change');
                }
                
                // Abre o modal
                document.getElementById("edit-modal").classList.remove("hidden");
                livroParaEditar = livroId;
            } else {
                alert("Não foi possível carregar os dados do livro para edição");
            }
        });
    });

    // ========== EVENTO: ABRIR MODAL DE EXCLUSÃO ==========
    const deleteIcons = document.querySelectorAll(".delete-icon");
    console.log(`Encontrados ${deleteIcons.length} ícones de exclusão`);
    
    deleteIcons.forEach((icon) => {
        icon.addEventListener("click", function() {
            const bookId = this.getAttribute("data-id");
            const row = this.closest("tr");
            const bookTitle = row.querySelector("td:nth-child(3)").textContent;
            
            console.log(`Clicou em excluir livro ID: ${bookId} - "${bookTitle}"`);
            
            livroParaExcluir = {
                id: bookId,
                element: row,
                title: bookTitle
            };
            
            // Mostra o título do livro no modal
            document.getElementById("delete-book-title").textContent = `"${bookTitle}"`;
            document.getElementById("delete-modal").classList.remove("hidden");
        });
    });

    // ========== FUNÇÃO: FECHAR TODOS OS MODAIS ==========
    function closeAllModals() {
        document.querySelectorAll(".modal").forEach(modal => {
            modal.classList.add("hidden");
        });
        livroParaExcluir = null;
        livroParaEditar = null;
        limparSelect2Autores();
        console.log("Todos os modais fechados");
    }

    // ========== EVENTO: FECHAR MODAIS ==========
    const closeButtons = document.querySelectorAll(".close-modal, .btn-cancelar");
    console.log(`Encontrados ${closeButtons.length} botões de fechar`);
    
    closeButtons.forEach((btn) => {
        btn.addEventListener("click", closeAllModals);
    });

    // ========== EVENTO: FECHAR MODAL AO CLICAR FORA ==========
    document.querySelectorAll(".modal").forEach((modal) => {
        modal.addEventListener("click", (e) => {
            if (e.target.classList.contains("modal")) {
                closeAllModals();
            }
        });
    });

    // ========== EVENTO: SUBMIT DO FORMULÁRIO DE EDIÇÃO ==========
    const editForm = document.getElementById("edit-form");
    if (editForm) {
        console.log("Formulário de edição encontrado");
        editForm.addEventListener("submit", async function(e) {
            e.preventDefault();
            console.log("Formulário de edição submetido");
            
            if (!livroParaEditar) {
                alert("Nenhum livro selecionado para edição");
                return;
            }
            
            // Pega os autores selecionados no Select2
            const autoresSelecionados = $('#edit-autores').val() || [];
            console.log("Autores selecionados:", autoresSelecionados);
            
            // IMPORTANTE: Agora use 'autores_ids' (plural)
            const formData = {
                titulo: document.getElementById("edit-titulo").value,
                editora_id: document.getElementById("edit-editora").value,
                ano_publicacao: document.getElementById("edit-ano").value,
                categoria_id: document.getElementById("edit-categoria").value,
                status_id: document.getElementById("edit-status").value,
                autores_ids: autoresSelecionados // Use 'autores_ids' (plural) aqui!
            };
            
            console.log("Dados para atualizar:", formData);
            
            const result = await updateLivro(livroParaEditar, formData);
            console.log("Resultado da atualização:", result);
            
            if (result.success) {
                alert("Livro atualizado com sucesso!");
                // Pequeno delay antes de recarregar
                setTimeout(() => {
                    location.reload();
                }, 500);
            } else {
                alert("Erro ao atualizar livro: " + (result.error || "Erro desconhecido"));
            }
        });
    } else {
        console.error("Formulário de edição NÃO encontrado!");
    }

    // ========== EVENTO: CONFIRMAR EXCLUSÃO ==========
    const confirmDeleteBtn = document.querySelector(".btn-confirmar-exclusao");
    if (confirmDeleteBtn) {
        confirmDeleteBtn.addEventListener("click", async () => {
            console.log("Botão de confirmação de exclusão clicado");
            
            if (!livroParaExcluir) {
                alert("Nenhum livro selecionado para exclusão");
                return;
            }
            
            const result = await deleteLivro(livroParaExcluir.id);
            console.log("Resultado da exclusão:", result);
            
            if (result.success) {
                // Remove a linha da tabela
                livroParaExcluir.element.remove();
                alert("Livro excluído com sucesso!");
            } else {
                alert("Erro ao excluir livro: " + (result.error || "Erro desconhecido"));
            }
            
            closeAllModals();
        });
    }

    // ========== EVENTO: BUSCA EM TEMPO REAL ==========
    const searchInput = document.getElementById("search-input");
    if (searchInput) {
        searchInput.addEventListener("input", function(e) {
            const searchTerm = e.target.value.toLowerCase();
            const rows = document.querySelectorAll(".tabela-livros tbody tr");
            let visibleCount = 0;
            
            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                if (text.includes(searchTerm)) {
                    row.style.display = "";
                    visibleCount++;
                } else {
                    row.style.display = "none";
                }
            });
            
            console.log(`Busca: "${searchTerm}" - ${visibleCount} livros encontrados`);
        });
    }
    
    console.log("Configuração de eventos concluída");
});