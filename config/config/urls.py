from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from biblioteca.views import login_view, tela_inicial, adicionar_livro, adicionar_autor, tela_todos_livros, adicionar_editora, adicionar_categoria

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('inicial/', tela_inicial, name='tela_inicial'),
    path('todosLivros/', tela_todos_livros, name='tela_todos_livros'),
    path('adicionarLivro/', adicionar_livro, name='adicionar_livro'),
    path('adicionarEditora/', adicionar_editora, name='adicionar_editora'),
    path('adicionarAutor/', adicionar_autor, name='adicionar_autor'),
    path('adicionarCategoria/', adicionar_categoria, name='adicionar_categoria'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)