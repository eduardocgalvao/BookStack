// utils.js
console.log("utils.js carregado");

// Variáveis globais (que precisam ser acessíveis entre módulos)
window.capaOriginalUrl = null;
window.novaCapaFile = null;
window.livroParaExcluir = null;
window.livroParaEditar = null;
window.autoresSelect2Instance = null;

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

window.csrftoken = getCookie('csrftoken');

// Função para fechar todos os modais
function closeAllModals() {
    document.querySelectorAll(".modal").forEach(modal => {
        modal.classList.add("hidden");
    });
    window.livroParaExcluir = null;
    window.livroParaEditar = null;
    
    // Limpa Select2 se existir
    if (window.autoresSelect2Instance) {
        window.autoresSelect2Instance.val(null).trigger('change');
    }
    
    console.log("Todos os modais fechados");
}
window.closeAllModals = closeAllModals;

// Validação de imagem
function validarImagem(file) {
    if (file.size > 5 * 1024 * 1024) {
        alert("A imagem é muito grande. Tamanho máximo: 5MB");
        return false;
    }
    
    const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp'];
    if (!validTypes.includes(file.type.toLowerCase())) {
        alert("Formato de imagem inválido. Use JPG, PNG, GIF ou WebP.");
        return false;
    }
    
    return true;
}
window.validarImagem = validarImagem;

// Log inicial
console.log("API_URLS:", window.API_URLS);
console.log("CSRF Token:", window.csrftoken ? "Encontrado" : "Não encontrado");