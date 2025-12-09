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
class LivroCreateForm(forms.ModelForm):
    class Meta:
        model = tbl_livro
        fields = "__all__"
        exclude = ['status']
        widgets = {
            "isbn": forms.TextInput(attrs={"class": "input-field"}),
            "titulo": forms.TextInput(attrs={"class": "input-field"}),
            "ano_publicacao": forms.NumberInput(attrs={"class": "input-field"}),
            "capa": forms.ClearableFileInput(attrs={"accept": "image/*"}),
            "editora": forms.Select(attrs={"class": "single-select"}),
            "quantidade": forms.NumberInput(attrs={"class": "input-field"}),
            "autores": Select2MultipleWidget(attrs={"class": "multi-select"}),
            "categorias": Select2MultipleWidget(attrs={"class": "multi-select"}),
        }

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
    senha = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = tbl_usuario
        fields = ["nome", "sobrenome", "email", "senha"]
        
        def save(self, commit=True):
            user = super().save(commit=False)
            user.set_password(self.cleaned_data['senha'])
            if commit:
                user.save()
            return user

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