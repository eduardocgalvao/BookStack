// eventos.js - EVENTOS PRINCIPAIS DA APLICAÇÃO
console.log("eventos.js carregado");

function setupEventListeners() {
    console.log("Configurando event listeners...");
    
    // ========== EVENTO: ABRIR MODAL DE EDIÇÃO ==========
    const editIcons = document.querySelectorAll(".edit-icon");
    console.log(`Encontrados ${editIcons.length} ícones de edição`);
    
    editIcons.forEach((icon) => {
        icon.addEventListener("click", async function() {
            const livroId = this.getAttribute("data-id");
            console.log(`Clicou em editar livro ID: ${livroId}`);

            // Resetar variáveis da capa
            window.capaOriginalUrl = null;
            window.novaCapaFile = null;
            const removeCapaCheckbox = document.getElementById('remove-capa');
            const capaInput = document.getElementById('edit-capa');
            
            if (removeCapaCheckbox) removeCapaCheckbox.checked = false;
            if (capaInput) capaInput.value = '';
            
            // Busca dados do livro
            const livro = await window.fetchLivro(livroId);
            if (livro) {
                console.log("Dados do livro para edição:", livro);
                
                // Preenche o formulário
                document.getElementById("edit-id").value = livro.id;
                document.getElementById("edit-titulo").value = livro.titulo || '';
                document.getElementById("edit-descricao").value = livro.descricao || ''; // ← ADICIONADO
                document.getElementById("edit-editora").value = livro.editora_id || '';
                document.getElementById("edit-ano").value = livro.ano_publicacao || '';
                
                if(document.getElementById("edit-quantidade")) {
                    document.getElementById("edit-quantidade").value = livro.quantidade || '';
                };

                // Preencher o status (CORRIGIDO: usar 'edit-status' em vez de 'edit-status-select')
                if (livro.status_id && document.getElementById('edit-status')) {
                    document.getElementById('edit-status').value = livro.status_id;
                    console.log("Status preenchido:", livro.status_id);
                }
                
                // Inicializa Select2 se ainda não foi
                if (window.inicializarSelect2Autores) {
                    window.inicializarSelect2Autores();
                }
                if (window.inicializarSelect2Categorias) {
                    window.inicializarSelect2Categorias();
                }

                // DEBUG: Verificar o que veio do backend
                console.log("Autores IDs recebidos:", livro.autores_ids);
                console.log("Categorias IDs recebidos:", livro.categorias_ids);
                console.log("Descrição recebida:", livro.descricao); // ← ADICIONADO
                
                // Preenche os autores no Select2
                if (livro.autores_ids && Array.isArray(livro.autores_ids)) {
                    $('#edit-autores').val(livro.autores_ids).trigger('change');
                    console.log("Autores preenchidos:", livro.autores_ids);
                } else {
                    $('#edit-autores').val(null).trigger('change');
                }

                // Preenche as categorias no Select2
                if (livro.categorias_ids && Array.isArray(livro.categorias_ids)) {
                    $('#edit-categoria').val(livro.categorias_ids).trigger('change');
                    console.log("Categorias preenchidas:", livro.categorias_ids);
                } else if (livro.categoria_ids && Array.isArray(livro.categoria_ids)) {
                    // Fallback para nome antigo (se existir)
                    $('#edit-categoria').val(livro.categoria_ids).trigger('change');
                } else {
                    $('#edit-categoria').val(null).trigger('change');
                }

                // Preenche a preview da capa
                const previewImg = document.getElementById('capa-preview-img');
                const placeholder = document.getElementById('capa-placeholder');
                
                if (livro.capa_url) {
                    window.capaOriginalUrl = livro.capa_url;
                    previewImg.src = livro.capa_url;
                    previewImg.style.display = 'block';
                    if (placeholder) placeholder.style.display = 'none';
                    console.log("Capa carregada:", livro.capa_url);
                } else {
                    previewImg.style.display = 'none';
                    if (placeholder) placeholder.style.display = 'flex';
                }
                
                // Abre o modal
                document.getElementById("edit-modal").classList.remove("hidden");
                window.livroParaEditar = livroId;
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
            
            window.livroParaExcluir = {
                id: bookId,
                element: row,
                title: bookTitle
            };
            
            // Mostra o título do livro no modal
            document.getElementById("delete-book-title").textContent = `"${bookTitle}"`;
            document.getElementById("delete-modal").classList.remove("hidden");
        });
    });

    // ========== EVENTO: MUDANÇA NA CAPA (PREVIEW E CAPTURA) ==========
    const capaInput = document.getElementById('edit-capa');
    const removeCapaCheckbox = document.getElementById('remove-capa');
    const previewImg = document.getElementById('capa-preview-img');
    const placeholder = document.getElementById('capa-placeholder');

    if (capaInput){
        capaInput.addEventListener('change', function(e) {
            const file = e.target.files[0];

            if(file) {
                // Salva arquivo na variável global
                window.novaCapaFile = file;
                console.log("Arquivo selecionado", file.name);

                // Cria o preview da imagem
                const reader = new FileReader();
                reader.onload = function(e){
                    if (previewImg) {
                        previewImg.src = e.target.result;
                        previewImg.style.display = 'block';

                    }
                    if (placeholder) placeholder.style.display = 'none';
                }
                reader.readAsDataURL(file);

                if (removeCapaCheckbox) removeCapaCheckbox.checked = false;
            }
        });
    }

    if (removeCapaCheckbox) {
        removeCapaCheckbox.addEventListener('change', function(){
            if (this.checked) {
                if (previewImg) previewImg.style.display = 'none';
                if (placeholder) placeholder.style.display = 'flex';

                if (capaInput) capaInput.value = '';
                window.novaCapaFile = null;
                console.log("Marcou para remover capa");
            } else {
                
                if (window.capaOriginalUrl && previewImg) {
                    previewImg.src = window.capaOriginalUrl;
                    previewImg.style.display = 'block';
                    if (placeholder) placeholder.style.display = 'none';
                }
            }
        });
    }

    // ========== EVENTO: SUBMIT DO FORMULÁRIO DE EDIÇÃO ==========
    const editForm = document.getElementById("edit-form");
    if (editForm) {
        console.log("Formulário de edição encontrado");
        editForm.addEventListener("submit", async function(e) {
            e.preventDefault();
            console.log("Formulário de edição submetido");
            
            if (!window.livroParaEditar) {
                alert("Nenhum livro selecionado para edição");
                return;
            }
            
            // Verifica se há uma nova capa ou se quer remover a capa
            const removeCapa = document.getElementById('remove-capa')?.checked || false;
            const temNovaCapa = window.novaCapaFile !== null;
            const deveEnviarFormData = temNovaCapa || removeCapa;
            
            // Pega os autores selecionados no Select2
            const autoresSelecionados = $('#edit-autores').val() || [];
            console.log("Autores selecionados:", autoresSelecionados);

            // Pega as categorias selecionadas no Select2
            const categoriasSelecionadas = $('#edit-categoria').val() || [];
            console.log("Categorias selecionadas:", categoriasSelecionadas);

            // Pega o status selecionado (CORRIGIDO: usar 'edit-status' em vez de 'edit-status-select')
            const statusSelecionado = $('#edit-status').val();
            console.log("Status selecionado:", statusSelecionado);
            
            // Pega a descrição do textarea ← ADICIONADO
            const descricao = document.getElementById('edit-descricao').value;
            console.log("Descrição a ser enviada:", descricao);
            
            let result;
            
            if (deveEnviarFormData) {
                // Usa FormData para enviar arquivos
                const formData = new FormData();
                
                // Adiciona campos básicos
                formData.append('titulo', document.getElementById("edit-titulo").value);
                formData.append('descricao', descricao); // ← ADICIONADO
                formData.append('editora_id', document.getElementById("edit-editora").value);
                formData.append('ano_publicacao', document.getElementById("edit-ano").value);
                formData.append('quantidade', document.getElementById('edit-quantidade').value);

                // Status
                if (statusSelecionado) {
                    formData.append('status_id', statusSelecionado);
                }
                
                // Adiciona autores como JSON string
                formData.append('autores_ids', JSON.stringify(autoresSelecionados));

                // Adiciona categorias como JSON string
                formData.append('categorias_ids', JSON.stringify(categoriasSelecionadas));
                
                // Adiciona capa se houver nova
                if (temNovaCapa) {
                    formData.append('capa', window.novaCapaFile);
                    console.log("Enviando nova capa:", window.novaCapaFile.name);
                }
                
                // Adiciona flag para remover capa
                if (removeCapa) {
                    formData.append('remove_capa', 'true');
                    console.log("Flag para remover capa enviada");
                }
                
                console.log("Enviando FormData com capa");
                result = await window.updateLivro(window.livroParaEditar, formData, true);
                
            } else {
                // Usa JSON normal (sem capa)
                const formData = {
                    titulo: document.getElementById("edit-titulo").value,
                    descricao: descricao, // ← ADICIONADO
                    editora_id: document.getElementById("edit-editora").value,
                    ano_publicacao: document.getElementById("edit-ano").value,
                    quantidade: document.getElementById("edit-quantidade").value,
                    autores_ids: autoresSelecionados,
                    categorias_ids: categoriasSelecionadas
                };

                // Status
                if (statusSelecionado) {
                    formData.status_id = statusSelecionado;
                }
                
                console.log("Enviando JSON sem capa");
                result = await window.updateLivro(window.livroParaEditar, formData, false);
            }
            
            console.log("Resultado da atualização:", result);
            
            if (result.success) {
                alert("Livro atualizado com sucesso!");
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
            
            if (!window.livroParaExcluir) {
                alert("Nenhum livro selecionado para exclusão");
                return;
            }
            
            const result = await window.deleteLivro(window.livroParaExcluir.id);
            console.log("Resultado da exclusão:", result);
            
            if (result.success) {
                // Remove a linha da tabela
                window.livroParaExcluir.element.remove();
                alert("Livro excluído com sucesso!");
            } else {
                alert("Erro ao excluir livro: " + (result.error || "Erro desconhecido"));
            }
            
            window.closeAllModals();
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
}
window.setupEventListeners = setupEventListeners;

// Configurar eventos quando o DOM carregar
document.addEventListener('DOMContentLoaded', setupEventListeners);