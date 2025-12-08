"""Views para gerenciamento de editoras."""
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from ..forms import EditoraForm
from ..models import tbl_editora

# LISTAR EDITORAS --------------------------------------------------------

class EditoraListView(View):
    template_name = "editora/editora_form.html"

    def get(self, request):
        editoras = tbl_editora.objects.all()
        return render(request, self.template_name, {"editoras": editoras})


#CRIAR EDITORA ----------------------------------------------------------

class EditoraCreateView(View):
    template_name = "editora/editora_form.html"

    def get(self, request):
        form = EditoraForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = EditoraForm(request.POST)
        if form.is_valid():
            editora = form.save()
            
            return render(request, self.template_name, {
                "form": form, 
                "sucesso": True, 
                "editora_id": editora.id_editora, 
                "editora_nome": editora.nome
            })

# EDITAR EDITORA ---------------------------------------------------------

class EditoraUpdateView(View):
    template_name = "editora/editora_form.html"

    def get(self, request, pk):
        editora = get_object_or_404(tbl_editora, pk=pk)
        form = EditoraForm(instance=editora)
        return render(request, self.template_name, {"form": form, "editora": editora})

    def post(self, request, pk):
        editora = get_object_or_404(tbl_editora, pk=pk)
        form = EditoraForm(request.POST, instance=editora)
        if form.is_valid():
            form.save()
            return redirect("editora-list")
        return render(request, self.template_name, {"form": form, "editora": editora})


# DELETAR EDITORA ---------------------------------------------------------

class EditoraDeleteView(View):
    template_name = "editora/editora_form.html"

    def get(self, request, pk):
        editora = get_object_or_404(tbl_editora, pk=pk)
        return render(request, self.template_name, {"editora": editora})

    def post(self, request, pk):
        editora = get_object_or_404(tbl_editora, pk=pk)
        editora.delete()
        return redirect("editora-list")
    
# LISTAR STATUS --------------------------------------------------------

class StatusLivroListView(View):
    template_name = "tela_inicial.html"

    def get(self, request):
        status_list = tbl_status_livro.objects.all()
        return render(request, self.template_name, {"status_list": status_list})