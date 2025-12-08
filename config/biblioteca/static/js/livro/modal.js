// modal.js - GERENCIAMENTO DE MODAIS
console.log("modal.js carregado");

function setupModalEvents() {
    // Evento: Fechar modais ao clicar nos botões
    const closeButtons = document.querySelectorAll(".close-modal, .btn-cancelar");
    console.log(`Encontrados ${closeButtons.length} botões de fechar`);
    
    closeButtons.forEach((btn) => {
        btn.addEventListener("click", window.closeAllModals);
    });

    // Evento: Fechar modal ao clicar fora
    document.querySelectorAll(".modal").forEach((modal) => {
        modal.addEventListener("click", (e) => {
            if (e.target.classList.contains("modal")) {
                window.closeAllModals();
            }
        });
    });
}
window.setupModalEvents = setupModalEvents;

// Configurar eventos quando o DOM carregar
document.addEventListener('DOMContentLoaded', setupModalEvents);