// todos_livros.js - VERSÃO CORRIGIDA
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

// DEBUG: Verifique se as URLs estão corretas
console.log("API_URLS:", window.API_URLS);
console.log("CSRF Token:", csrftoken ? "Encontrado" : "Não encontrado");

// Funções AJAX com tratamento de erro melhorado
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

// Verifica se os elementos existem antes de adicionar event listeners
document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM carregado, configurando eventos...");
    
    // Abre o modal de edição
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
                document.getElementById("edit-editora").value = livro.editora || '';
                document.getElementById("edit-autores").value = livro.autores || '';
                document.getElementById("edit-ano").value = livro.ano_publicacao || '';
                document.getElementById("edit-categoria").value = livro.categoria_id || '';
                document.getElementById("edit-status").value = livro.status || 'ativo';
                
                // Abre o modal
                document.getElementById("edit-modal").classList.remove("hidden");
                livroParaEditar = livroId;
            } else {
                alert("Não foi possível carregar os dados do livro para edição");
            }
        });
    });

    // Abre o modal de exclusão
    const deleteIcons = document.querySelectorAll(".delete-icon");
    console.log(`Encontrados ${deleteIcons.length} ícones de exclusão`);
    
    deleteIcons.forEach((icon) => {
        icon.addEventListener("click", function() {
            const bookId = this.getAttribute("data-id");
            const row = this.closest("tr");
            const bookTitle = row.querySelector("td:nth-child(2)").textContent;
            
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

    // Fecha modais
    function closeAllModals() {
        document.querySelectorAll(".modal").forEach(modal => {
            modal.classList.add("hidden");
        });
        livroParaExcluir = null;
        livroParaEditar = null;
        console.log("Todos os modais fechados");
    }

    const closeButtons = document.querySelectorAll(".close-modal, .btn-cancelar");
    console.log(`Encontrados ${closeButtons.length} botões de fechar`);
    
    closeButtons.forEach((btn) => {
        btn.addEventListener("click", closeAllModals);
    });

    // Fecha modais ao clicar fora
    document.querySelectorAll(".modal").forEach((modal) => {
        modal.addEventListener("click", (e) => {
            if (e.target.classList.contains("modal")) {
                closeAllModals();
            }
        });
    });

    // Submissão do formulário de edição
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
            
            const formData = {
                titulo: document.getElementById("edit-titulo").value,
                editora: document.getElementById("edit-editora").value,
                autores: document.getElementById("edit-autores").value,
                ano_publicacao: document.getElementById("edit-ano").value,
                categoria_id: document.getElementById("edit-categoria").value,
                status: document.getElementById("edit-status").value
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

    // Confirma exclusão
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

    // Busca em tempo real
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