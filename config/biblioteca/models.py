from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
import os


# =========================================
# EDITORA
# =========================================
class tbl_editora(models.Model):
    id_editora = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    endereco = models.CharField(max_length=200)
    cidade = models.CharField(max_length=200)

    class Meta:
        db_table = "tbl_editora"
        verbose_name = "Editora"
        verbose_name_plural = "Editoras"

    def __str__(self):
        return self.nome


# =========================================
# AUTOR
# =========================================
class tbl_autor(models.Model):
    id_autor = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    sobrenome = models.CharField(max_length=255)

    class Meta:
        db_table = "tbl_autor"
        verbose_name = "Autor"
        verbose_name_plural = "Autores"

    def __str__(self):
        return f"{self.nome} {self.sobrenome}"


# =========================================
# CATEGORIA
# =========================================
class tbl_categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)

    class Meta:
        db_table = "tbl_categoria"
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.nome


# =========================================
# STATUS DO LIVRO
# =========================================
class tbl_status_livro(models.Model):
    id_status = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=255, unique=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        db_table = "tbl_status_livro"
        verbose_name = "Status do Livro"
        verbose_name_plural = "Status dos Livros"

    def __str__(self):
        return self.descricao


# =========================================
# CAMINHO DA CAPA
# =========================================
def livro_capa_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    nome_arquivo = f"capa_{instance.id_livro}.{ext}"
    return os.path.join("capas_livros", nome_arquivo)


# =========================================
# LIVRO
# =========================================
class tbl_livro(models.Model):
    id_livro = models.AutoField(primary_key=True)
    isbn = models.CharField(max_length=20)
    titulo = models.CharField(max_length=255)
    ano_publicacao = models.IntegerField()
    descricao = models.TextField(blank=True, null=True)
    quantidade = models.IntegerField(default=0)  # Estoque total (NUNCA muda)
    disponivel = models.IntegerField(default=0)  # Disponíveis para empréstimo (VARIÁVEL)

    editora = models.ForeignKey(tbl_editora, on_delete=models.PROTECT)
    status = models.ForeignKey(tbl_status_livro, on_delete=models.PROTECT)

    capa = models.ImageField(
        upload_to=livro_capa_upload_path,
        null=True,
        blank=True
    )

    autores = models.ManyToManyField(tbl_autor, through="tbl_livro_autor")
    categorias = models.ManyToManyField(tbl_categoria, through="tbl_livro_categoria")

    dt_criacao = models.DateTimeField(auto_now_add=True)
    dt_atualizacao = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        try:
            self.quantidade = int(self.quantidade)
            self.disponivel = int(self.disponivel)
        except (TypeError, ValueError):
            self.quantidade = 0
            self.disponivel = 0

        # Na primeira criação, define disponivel = quantidade
        if not self.pk and self.disponivel == 0 and self.quantidade > 0:
            self.disponivel = self.quantidade
        else:
            # Verifica se quantidade foi alterada manualmente
            try:
                original = tbl_livro.objects.get(pk=self.pk)

            # Se quantidade foi alterada, ajusta disponivel proporcionalmente
                if self.disponivel < 0:
                    self.disponivel = 0

            except tbl_livro.DoesNotExist:
                pass
            
        # Só define status automaticamente se ainda não foi definido manualmente
        if not self.status_id:
        
            status_map = {
                "Disponível": self.disponivel > 0,
                "Indisponível": self.disponivel <= 0,
            }

            for descricao, condicao in status_map.items():
                if condicao:
                    try:
                        self.status = tbl_status_livro.objects.get(descricao=descricao)
                    except tbl_status_livro.DoesNotExist:
                        raise ValueError(
                            f"Status obrigatório '{descricao}' não existe no banco."
                        )
                    break

        super().save(*args, **kwargs)



# =========================================
# LIVRO x AUTOR
# =========================================
class tbl_livro_autor(models.Model):
    livro = models.ForeignKey(tbl_livro, on_delete=models.CASCADE)
    autor = models.ForeignKey(tbl_autor, on_delete=models.CASCADE)

    class Meta:
        db_table = "tbl_livro_autor"
        unique_together = ("livro", "autor")


# =========================================
# LIVRO x CATEGORIA
# =========================================
class tbl_livro_categoria(models.Model):
    livro = models.ForeignKey(tbl_livro, on_delete=models.CASCADE)
    categoria = models.ForeignKey(tbl_categoria, on_delete=models.CASCADE)

    class Meta:
        db_table = "tbl_livro_categoria"
        unique_together = ("livro", "categoria")


# =========================================
# USUÁRIO
# =========================================
class UsuarioManager(BaseUserManager):
    def create_user(self, email, nome, sobrenome, password=None):
        if not email:
            raise ValueError("E-mail obrigatório")

        email = self.normalize_email(email)
        user = self.model(email=email, nome=nome, sobrenome=sobrenome)
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

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nome", "sobrenome"]

    def __str__(self):
        return self.email


# =========================================
# ALUNO
# =========================================
class Aluno(models.Model):
    nome = models.CharField(max_length=200)
    sobrenome = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    matricula = models.CharField(max_length=50, unique=True)
    ativo = models.BooleanField(default=True)

    dt_criacao = models.DateTimeField(auto_now_add=True)
    dt_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tbl_aluno"
        verbose_name = "Aluno"
        verbose_name_plural = "Alunos"
        ordering = ["nome"]

    def __str__(self):
        return f"{self.nome} {self.sobrenome}"


# =========================================
# EMPRÉSTIMO
# =========================================
class Emprestimo(models.Model):
    STATUS_CHOICES = [
        ("ativo", "Ativo"),
        ("devolvido", "Devolvido"),
        ("atrasado", "Atrasado"),
        ("cancelado", "Cancelado"),
    ]

    livro = models.ForeignKey(tbl_livro, on_delete=models.PROTECT, related_name="emprestimos")
    aluno = models.ForeignKey(Aluno, on_delete=models.PROTECT, related_name="emprestimos")
    funcionario = models.ForeignKey(tbl_usuario, on_delete=models.PROTECT)

    dt_emprestimo = models.DateTimeField(default=timezone.now)
    dt_devolucao_prevista = models.DateField()
    dt_devolucao_real = models.DateTimeField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ativo")
    observacoes = models.TextField(blank=True, null=True)

    dt_criacao = models.DateTimeField(auto_now_add=True)
    dt_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tbl_emprestimo"
        verbose_name = "Empréstimo"
        verbose_name_plural = "Empréstimos"

    def __str__(self):
        return f"{self.livro.titulo} - {self.aluno.nome}"

class tbl_motivo_remocao(models.Model):
    id_motivo = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=255)

    class Meta:
        db_table = "tbl_motivo_remocao"
        verbose_name = "Motivo de Remoção"
        verbose_name_plural = "Motivos de Remoção"

    def __str__(self):
        return self.descricao

class tbl_livro_remocao(models.Model):
    id_remocao = models.AutoField(primary_key=True)
    livro = models.ForeignKey('tbl_livro', on_delete=models.PROTECT)
    motivo = models.ForeignKey(tbl_motivo_remocao, on_delete=models.PROTECT)
    dt_remocao = models.DateTimeField(auto_now_add=True)
    removido_por = models.ForeignKey('tbl_usuario', on_delete=models.PROTECT)

    class Meta:
        db_table = "tbl_livro_remocao"
        verbose_name = "Remoção de Livro"
        verbose_name_plural = "Remoções de Livros"
