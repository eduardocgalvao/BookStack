# biblioteca/urls.py
from django.urls import path

from .views.livro_views import (
    livro_list,
    LivroCreateView,
    api_livro_detail,
    api_livro_update,
    api_livro_delete,
    RemoverLivroView,
    AssociarAutorView,
    AssociarCategoriaView,
)

from .views import (
    home_view,
    login_view,
    AutorListView,
    AutorCreateView,
    AutorUpdateView,
    AutorDeleteView,
    CategoriaListView,
    CategoriaCreateView,
    CategoriaUpdateView,
    CategoriaDeleteView,
    EditoraListView,
    EditoraCreateView,
    EditoraUpdateView,
    EditoraDeleteView,
    StatusLivroListView, 
    StatusLivroCreateView,
    StatusLivroUpdateView,
    StatusLivroDeleteView,
    UsuarioListView,
    UsuarioCreateView,
    UsuarioUpdateView,
    UsuarioDeleteView,
    MotivoRemocaoListView,
    MotivoRemocaoCreateView,
    MotivoRemocaoUpdateView,
    MotivoRemocaoDeleteView,
    home,
    registro_view,
    buscar_alunos, 
    registrar_emprestimo, 
    # emprestimo_list
)

# View para o modal
from .views.home_view import livro_dados_json  # Adicione esta linha
from .views.home_view import listar_livros  # Adicione esta linha se necessário

urlpatterns = [
    # LOGIN
    path("", login_view, name="login"),
    path("registro/", registro_view, name="registro"),

    # TELA INICIAL (HOME)
    path('home/', listar_livros, name='home'),  # Use listar_livros
    
    # API para dados do livro (para o modal)
    path('dados-livro/<int:livro_id>/', livro_dados_json, name='livro_dados_json'),
    
    # API para livros
    path("api/livro/<int:livro_id>/", api_livro_detail, name="api_livro_detail"),
    path("api/livro/<int:livro_id>/update/", api_livro_update, name="api_livro_update"),
    path("api/livro/<int:livro_id>/delete/", api_livro_delete, name="api_livro_delete"),
    
    # LIVROS
    path("livro/novo/", LivroCreateView.as_view(), name="livro-create"),
    path("livro/list/", livro_list, name="livro-list"),
    
    # EMPRÉSTIMOS
    path('emprestimo/registrar/', registrar_emprestimo, name='registrar_emprestimo'),
    path('emprestimo/buscar-alunos/', buscar_alunos, name='buscar_alunos'),
    # path('emprestimos/', emprestimo_list, name='emprestimo-list'),
    
    # AUTORES
    path("autores/", AutorListView.as_view(), name="autor-list"),
    path("autores/novo/", AutorCreateView.as_view(), name="autor-create"),
    path("autores/<int:pk>/editar/", AutorUpdateView.as_view(), name="autor-update"),
    path("autores/<int:pk>/deletar/", AutorDeleteView.as_view(), name="autor-delete"),
    
    # CATEGORIAS
    path("categorias/", CategoriaListView.as_view(), name="categoria-list"),
    path("categorias/novo/", CategoriaCreateView.as_view(), name="categoria-create"),
    path("categorias/<int:pk>/editar/", CategoriaUpdateView.as_view(), name="categoria-update"),
    path("categorias/<int:pk>/deletar/", CategoriaDeleteView.as_view(), name="categoria-delete"),
    
    # EDITORAS
    path("editoras/", EditoraListView.as_view(), name="editora-list"),
    path("editoras/novo/", EditoraCreateView.as_view(), name="editora-create"),
    path("editoras/<int:pk>/editar/", EditoraUpdateView.as_view(), name="editora-update"),
    path("editoras/<int:pk>/deletar/", EditoraDeleteView.as_view(), name="editora-delete"),
    
    # STATUS DO LIVRO
    path("status/", StatusLivroListView.as_view(), name="status-list"),
    path("status/novo/", StatusLivroCreateView.as_view(), name="status-create"),
    path("status/<int:pk>/editar/", StatusLivroUpdateView.as_view(), name="status-update"),
    path("status/<int:pk>/deletar/", StatusLivroDeleteView.as_view(), name="status-delete"),
    
    # USUÁRIOS
    path("usuarios/", UsuarioListView.as_view(), name="usuario-list"),
    path("usuarios/novo/", UsuarioCreateView.as_view(), name="usuario-create"),
    path("usuarios/<int:pk>/editar/", UsuarioUpdateView.as_view(), name="usuario-update"),
    path("usuarios/<int:pk>/deletar/", UsuarioDeleteView.as_view(), name="usuario-delete"),
    
    # MOTIVOS DE REMOÇÃO
    path("motivos/", MotivoRemocaoListView.as_view(), name="motivo-list"),
    path("motivos/novo/", MotivoRemocaoCreateView.as_view(), name="motivo-create"),
    path("motivos/<int:pk>/editar/", MotivoRemocaoUpdateView.as_view(), name="motivo-update"),
    path("motivos/<int:pk>/deletar/", MotivoRemocaoDeleteView.as_view(), name="motivo-delete"),
    
    # ASSOCIAÇÃO LIVRO-AUTOR
    path("livros/<int:pk>/autores/", AssociarAutorView.as_view(), name="livro-autores"),
    
    # ASSOCIAÇÃO LIVRO-CATEGORIA
    path("livros/<int:pk>/categorias/", AssociarCategoriaView.as_view(), name="livro-categorias"),
    
    # REMOVER LIVRO
    path("livros/<int:pk>/remover/", RemoverLivroView.as_view(), name="livro-remover"),
]