"""Exporta todas as views."""
from .auth_views import (login_view, tela_inicial)
from .livro_views import (
    LivroCreateView, livro_list, RemoverLivroView,
    AssociarAutorView, AssociarCategoriaView
)
from .autor_views import (
    AutorListView, AutorCreateView, AutorUpdateView, AutorDeleteView
)
from .categoria_views import (
    CategoriaListView, CategoriaCreateView, 
    CategoriaUpdateView, CategoriaDeleteView
)
from .editora_views import (
    EditoraListView, EditoraCreateView,
    EditoraUpdateView, EditoraDeleteView
)
from .outros_views import (
    StatusLivroListView, StatusLivroCreateView,
    StatusLivroUpdateView, StatusLivroDeleteView,
    UsuarioListView, UsuarioCreateView,
    UsuarioUpdateView, UsuarioDeleteView,
    MotivoRemocaoListView, MotivoRemocaoCreateView,
    MotivoRemocaoUpdateView, MotivoRemocaoDeleteView
)

# Exportações gerais
__all__ = [
    'login_view', 'tela_inicial', 'tela_todos_livros',
    'LivroCreateView', 'RemoverLivroView',
    'AssociarAutorView', 'AssociarCategoriaView',
    'AutorListView', 'AutorCreateView', 'AutorUpdateView', 'AutorDeleteView',
    'CategoriaListView', 'CategoriaCreateView', 
    'CategoriaUpdateView', 'CategoriaDeleteView',
    'EditoraListView', 'EditoraCreateView',
    'EditoraUpdateView', 'EditoraDeleteView',
    # ... outras exportações
]