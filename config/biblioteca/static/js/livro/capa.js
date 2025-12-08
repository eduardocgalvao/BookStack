// capa.js - GERENCIAMENTO DE CAPAS
console.log("capa.js carregado");

function setupCapaEvents() {
    // Evento: Mudança na input de capa
    const capaInput = document.getElementById('edit-capa');
    if (capaInput) {
        capaInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                // Valida a imagem
                if (!window.validarImagem(file)) {
                    this.value = '';
                    return;
                }
                
                window.novaCapaFile = file;
                
                // Criar preview
                const reader = new FileReader();
                reader.onload = function(e) {
                    const previewImg = document.getElementById('capa-preview-img');
                    const placeholder = document.getElementById('capa-placeholder');
                    
                    if (previewImg) {
                        previewImg.src = e.target.result;
                        previewImg.style.display = 'block';
                    }
                    if (placeholder) placeholder.style.display = 'none';
                };
                reader.readAsDataURL(file);
                
                // Desmarcar o checkbox de remover capa
                const removeCapaCheckbox = document.getElementById('remove-capa');
                if (removeCapaCheckbox) removeCapaCheckbox.checked = false;
                
                console.log("Nova capa selecionada:", file.name);
            }
        });
    }

    // Evento: Remover capa
    const removeCapaCheckbox = document.getElementById('remove-capa');
    if (removeCapaCheckbox) {
        removeCapaCheckbox.addEventListener('change', function(e) {
            if (this.checked) {
                // Limpar o input de arquivo
                const capaInput = document.getElementById('edit-capa');
                if (capaInput) capaInput.value = '';
                window.novaCapaFile = null;
                
                // Mostrar placeholder
                const previewImg = document.getElementById('capa-preview-img');
                const placeholder = document.getElementById('capa-placeholder');
                
                if (previewImg) previewImg.style.display = 'none';
                if (placeholder) placeholder.style.display = 'flex';
                
                console.log("Remover capa ativado");
            }
        });
    }
}
window.setupCapaEvents = setupCapaEvents;

// Configurar eventos quando o DOM carregar
document.addEventListener('DOMContentLoaded', setupCapaEvents);