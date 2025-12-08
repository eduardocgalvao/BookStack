"""Views para gerenciamento de autores."""
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from ..forms import AutorForm
from ..models import tbl_autor

class AutorCRUDMixin:
    """Mixin com funcionalidades comuns para CRUD."""
    template_name = None
    form_class = None
    model_class = None
    redirect_url = None
    
    def get_context_data(self, **kwargs):
        """Retorna contexto padrão para templates."""
        context = kwargs
        if 'form' not in context:
            context['form'] = self.form_class()
        return context

class AutorListView(View, AutorCRUDMixin):
    """View para listar autores."""
    template_name = "autor/autor_form.html"
    model_class = tbl_autor
    
    def get(self, request):
        autores = self.model_class.objects.all()
        return render(request, self.template_name, {"autores": autores})

class AutorCreateView(View, AutorCRUDMixin):
    template_name = "autor/autor_form.html"
    form_class = AutorForm
    model_class = tbl_autor
    
    def get(self, request):
        autores = self.model_class.objects.all()
        return render(request, self.template_name, {"form": self.form_class(), "autores": autores})
        
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            autor = form.save()
            autores = self.model_class.objects.all()
            return render(request, self.template_name, {
                "form": self.form_class(),
                "autores": autores,
                "sucesso": True,
                "autor_id": autor.id_autor,
                "autor_nome": autor.nome,
                "autor_sobrenome": autor.sobrenome
            })
        autores = self.model_class.objects.all()
        return render(request, self.template_name, {"form": form, "autores": autores})


class AutorUpdateView(View, AutorCRUDMixin):
    """View para atualizar um autor existente."""
    template_name = "autor/autor_form.html"
    form_class = AutorForm
    model_class = tbl_autor
    redirect_url = "autor-list"
    
    def get(self, request, pk):
        autor = get_object_or_404(self.model_class, pk=pk)
        form = self.form_class(instance=autor)
        return render(request, self.template_name, self.get_context_data(form=form, autor=autor))

    def post(self, request, pk):
        autor = get_object_or_404(self.model_class, pk=pk)
        form = self.form_class(request.POST, instance=autor)
        if form.is_valid():
            form.save()
            return redirect(self.redirect_url)
        return render(request, self.template_name, self.get_context_data(form=form, autor=autor))

class AutorDeleteView(View, AutorCRUDMixin):
    """View para deletar um autor."""
    template_name = "autor/autor_form.html"
    model_class = tbl_autor
    redirect_url = "autor-list"
    
    def get(self, request, pk):
        autor = get_object_or_404(self.model_class, pk=pk)
        return render(request, self.template_name, self.get_context_data(autor=autor))

    def post(self, request, pk):
        autor = get_object_or_404(self.model_class, pk=pk)
        autor.delete()
        return redirect(self.redirect_url)