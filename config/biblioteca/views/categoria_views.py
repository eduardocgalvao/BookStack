"""Views para gerenciamento de categorias."""
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from ..forms import CategoriaForm
from ..models import tbl_categoria

class CategoriaListView(View):
    template_name = "categoria/categoria_form.html"

    def get(self, request):
        categorias = tbl_categoria.objects.all()
        return render(request, self.template_name, {"categorias": categorias})

class CategoriaCreateView(View):
    template_name = "categoria/categoria_form.html"

    def get(self, request):
        form = CategoriaForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = CategoriaForm(request.POST)
        if form.is_valid():
            categoria = form.save()

            return render(request, self.template_name, {
                "form": CategoriaForm(),
                "sucesso": True,
                "categoria_id": categoria.id_categoria,
                "categoria_nome": categoria.nome
            })

        return render(request, self.template_name, {"form": form})
class CategoriaUpdateView(View):
    template_name = "categoria/categoria_form.html"

    def get(self, request, pk):
        categoria = get_object_or_404(tbl_categoria, pk=pk)
        form = CategoriaForm(instance=categoria)
        return render(request, self.template_name, {"form": form, "categoria": categoria})

    def post(self, request, pk):
        categoria = get_object_or_404(tbl_categoria, pk=pk)
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect("categoria-list")
        return render(request, self.template_name, {"form": form, "categoria": categoria})

class CategoriaDeleteView(View):
    template_name = "categoria/categoria_form.html"

    def get(self, request, pk):
        categoria = get_object_or_404(tbl_categoria, pk=pk)
        return render(request, self.template_name, {"categoria": categoria})

    def post(self, request, pk):
        categoria = get_object_or_404(tbl_categoria, pk=pk)
        categoria.delete()
        return redirect("categoria-list")