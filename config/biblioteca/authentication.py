"""
Backend de autenticação customizado que usa tbl_usuario ao invés de User padrão.

Configurar em settings.py:
AUTHENTICATION_BACKENDS = ['biblioteca.authentication.TblUsuarioBackend']
"""

from django.contrib.auth.backends import ModelBackend
from .models import tbl_usuario


class TblUsuarioBackend(ModelBackend):
    """Backend customizado para autenticar via tbl_usuario."""
    
    def authenticate(self, request, email=None, **kwargs):
        """Autentica usuário pelo email."""
        try:
            return tbl_usuario.objects.get(email=email)
        except tbl_usuario.DoesNotExist:
            return None
    
    def get_user(self, user_id):
        """Recupera usuário pela chave primária (id_usuario)."""
        try:
            return tbl_usuario.objects.get(id_usuario=user_id)
        except tbl_usuario.DoesNotExist:
            return None
    
    def get_user_permissions(self, user_obj):
        """Retorna permissões vazias (não utiliza sistema de permissões)."""
        return set()
    
    def get_group_permissions(self, user_obj):
        """Retorna permissões de grupo vazias."""
        return set()
    
    def get_all_permissions(self, user_obj):
        """Retorna todas as permissões vazias."""
        return set()


