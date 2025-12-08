// select2.js - CONFIGURAÇÃO DO PLUGIN SELECT2
console.log("select2.js carregado");

// Variável global para instância de autores
window.autoresSelect2Instance = null;
// Variável para instância de categorias
window.categoriasSelect2Instance = null;

function inicializarSelect2Autores() {
    if (!window.autoresSelect2Instance && $('#edit-autores').length) {
        window.autoresSelect2Instance = $('#edit-autores').select2({
            width: '100%',
            placeholder: 'Selecione os autores',
            allowClear: true,
            dropdownParent: $('#edit-modal')
        });
        console.log("Select2 inicializado para autores");
    }
}
window.inicializarSelect2Autores = inicializarSelect2Autores;

function inicializarSelect2Categorias() {
    if (!window.categoriasSelect2Instance && $('#edit-categoria').length) {
        window.categoriasSelect2Instance = $('#edit-categoria').select2({
            width: '100%',
            placeholder: 'Selecione as categorias',
            allowClear: true,
            dropdownParent: $('#edit-modal')
        });
        console.log("Select2 inicializado para categorias");
    }
}
window.inicializarSelect2Categorias = inicializarSelect2Categorias;

function limparSelect2Autores() {
    if (window.autoresSelect2Instance) {
        window.autoresSelect2Instance.val(null).trigger('change');
    }
}
window.limparSelect2Autores = limparSelect2Autores;

function limparSelect2Categorias() {
    if (window.categoriasSelect2Instance) {
        window.categoriasSelect2Instance.val(null).trigger('change');
    }
}
window.limparSelect2Categorias = limparSelect2Categorias;

// Inicializar Select2 quando o DOM carregar
document.addEventListener('DOMContentLoaded', function() {
    // Inicializa Select2 para autores se o elemento existir
    if ($('#edit-autores').length) {
        inicializarSelect2Autores();
    }
    
    // Inicializa Select2 para categorias se o elemento existir
    if ($('#edit-categoria').length) {
        inicializarSelect2Categorias();
    }
});