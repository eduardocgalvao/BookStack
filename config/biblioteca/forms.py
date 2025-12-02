from django import forms
from django_select2.forms import Select2MultipleWidget

from .models import (
    tbl_editora, 
    tbl_autor, 
    tbl_categoria, 
    tbl_status_livro,
    tbl_usuario,
    tbl_motivo_remocao,
    tbl_livro
)
# Formulário para criação de um novo livro
class LivroCreateForm(forms.Form):
    isbn = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'input-field'})
    )

    titulo = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'input-field'})
    )

    ano_publicacao = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'input-field'})
    )

    editora = forms.ModelChoiceField(
        queryset=tbl_editora.objects.all(),
        widget=forms.Select(attrs={'class': 'single-select'})
    )

    status = forms.ModelChoiceField(
        queryset=tbl_status_livro.objects.all(),
        widget=forms.Select(attrs={'class': 'single-select'})
    )

    autores = forms.ModelMultipleChoiceField(
        queryset=tbl_autor.objects.all(),
        widget=Select2MultipleWidget(attrs={'class': 'multi-select'}),
        required=False
    )

    categorias = forms.ModelMultipleChoiceField(
        queryset=tbl_categoria.objects.all(),
        widget=Select2MultipleWidget(attrs={'class': 'multi-select'}),
        required=False
    )


# Formulário autor
class AutorForm(forms.ModelForm):
    class Meta:
        model = tbl_autor
        fields = ["nome", "sobrenome"]

# Formulário categoria
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = tbl_categoria
        fields = ['nome']

# Formulário editora
class EditoraForm(forms.ModelForm):
    class Meta:
        model = tbl_editora
        fields = ['nome', 'cidade', 'endereco']

# Formulário Status do Livro
class StatusLivroForm(forms.ModelForm):
    class Meta:
        model = tbl_status_livro
        fields = ['descricao']

# Formulário Usuários
class UsuarioForm(forms.ModelForm):
    class Meta:
        model = tbl_usuario
        fields = ["nome", "sobrenome", "email"]

# Formulário Motivo Da Remoção
class MotivoRemocaoForm(forms.ModelForm):
    class Meta:
        model = tbl_motivo_remocao
        fields = ["descricao"]

# Formulário Escolher Autor
class LivroAutorForm(forms.Form):
    autores = forms.ModelMultipleChoiceField(
        queryset=tbl_autor.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Selecione os autores"
)

# Associar livro a categorias
class LivroCategoriaForm(forms.Form):
    categorias = forms.ModelMultipleChoiceField(
        queryset=tbl_categoria.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Selecione as categorias"
)
    
# Formulário Remoção de Livro
class RemoverLivroForm(forms.Form):
    motivo = forms.ModelChoiceField(
        queryset=tbl_motivo_remocao.objects.all(),
        label="Motivo da Remoção",
        required=True
    )

    removido_por = forms.ModelChoiceField(
        queryset=tbl_usuario.objects.all(),
        label="Removido por",
        required=True
    )