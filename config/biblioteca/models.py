"""Modelos de banco de dados para o sistema de biblioteca."""

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import os

class tbl_editora(models.Model):
    """Armazena informações das editoras de livros."""
    id_editora = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    endereco = models.CharField(max_length=200)
    cidade = models.CharField(max_length=200)

    def __str__(self):
        return self.nome


class tbl_autor(models.Model):
    """Armazena dados dos autores de livros."""
    id_autor = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    sobrenome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome


class tbl_categoria(models.Model):
    """Define as categorias/gêneros de livros."""
    id_categoria = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

class tbl_status_livro(models.Model):
    """Define os possíveis status de um livro (ativo, inativo, removido, etc)."""
    id_status = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=255)
    ativo = models.BooleanField(default=True)
    
    class Meta:
        db_table = "tbl_status_livro"
        verbose_name = "Status do Livro"
        verbose_name_plural = "Status dos Livros"

    def __str__(self):
        return self.descricao

# Função para definir o caminho de upload da capa do livro
def livro_capa_upload_path(instance, filename):
    """Define o caminho de upload para capas de livros."""
    # Gera um nome único baseado no ID do livro
    ext = filename.split('.')[-1]
    filename = f"capa_{instance.id_livro}.{ext}"
    return os.path.join('capas_livros', filename)

class tbl_livro(models.Model):
    """Tabela principal com informações dos livros do acervo."""
    id_livro = models.AutoField(primary_key=True)
    isbn = models.CharField(max_length=20)
    titulo = models.CharField(max_length=255)
    ano_publicacao = models.IntegerField()
    quantidade = models.IntegerField(default=0)
    editora = models.ForeignKey(tbl_editora, on_delete=models.PROTECT)
    status = models.ForeignKey(tbl_status_livro, on_delete=models.PROTECT, )
    capa = models.ImageField(
        upload_to=livro_capa_upload_path, 
        null=True, 
        blank=True, 
        verbose_name="Capa do Livro")
    # Relacionamentos Many-to-Many com tabelas de associação
    autores = models.ManyToManyField(tbl_autor, through="tbl_livro_autor")
    categorias = models.ManyToManyField(tbl_categoria, through="tbl_livro_categoria")
    dt_criacao = models.DateTimeField(auto_now_add=True)
    dt_atualizacao = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):

        
        if self.quantidade is not None:
            try:
                self.quantidade = int(self.quantidade)
            except ValueError:
                self.quantidade = 0
        # Atualiza o status automaticamente baseado na quantidade

        if self.quantidade > 0:
            self.status = tbl_status_livro.objects.get(descricao="Disponível")
        else:
            self.status = tbl_status_livro.objects.get(descricao="Indisponível")

        super().save(*args, **kwargs)


class tbl_livro_autor(models.Model):
    """Tabela de associação Many-to-Many entre livros e autores."""
    livro = models.ForeignKey(tbl_livro, on_delete=models.CASCADE)
    autor = models.ForeignKey(tbl_autor, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('livro', 'autor')  # Impede duplicação de registros


class tbl_livro_categoria(models.Model):
    """Tabela de associação Many-to-Many entre livros e categorias."""
    livro = models.ForeignKey(tbl_livro, on_delete=models.CASCADE)
    categoria = models.ForeignKey(tbl_categoria, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('livro', 'categoria')  # Impede duplicação de registros

class UsuarioManager(BaseUserManager):
    def create_user(self, email, nome, sobrenome, password=None):
        if not email:
            raise ValueError("O usuário precisa de um e-mail")

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            nome=nome,
            sobrenome=sobrenome
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nome, sobrenome, password):
        user = self.create_user(email, nome, sobrenome, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    
class tbl_usuario(AbstractBaseUser, PermissionsMixin):
    id_usuario = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    sobrenome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'sobrenome']

    def __str__(self):
        return self.email

class tbl_motivo_remocao(models.Model):
    """Define os motivos pelos quais um livro pode ser removido do acervo."""
    id_motivo = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=255)


class tbl_livro_remocao(models.Model):
    """Registra o histórico de remoções de livros do acervo."""
    id_remocao = models.AutoField(primary_key=True)
    livro = models.ForeignKey(tbl_livro, on_delete=models.PROTECT)
    motivo = models.ForeignKey(tbl_motivo_remocao, on_delete=models.PROTECT)
    dt_remocao = models.DateTimeField(auto_now_add=True)
    removido_por = models.ForeignKey(tbl_usuario, on_delete=models.PROTECT)
