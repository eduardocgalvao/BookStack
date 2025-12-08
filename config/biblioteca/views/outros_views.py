"""Views para entidades diversas."""
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from ..forms import StatusLivroForm, UsuarioForm, MotivoRemocaoForm
from ..models import tbl_status_livro, tbl_usuario, tbl_motivo_remocao

# LISTAR STATUS --------------------------------------------------------

class StatusLivroListView(View):
    template_name = "dashboard/home.html"

    def get(self, request):
        status_list = tbl_status_livro.objects.all()
        return render(request, self.template_name, {"status_list": status_list})


# CRIAR STATUS ---------------------------------------------------------

class StatusLivroCreateView(View):
    template_name = "dashboard/home.html"

    def get(self, request):
        form = StatusLivroForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = StatusLivroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("status-list")
        return render(request, self.template_name, {"form": form})


# EDITAR STATUS --------------------------------------------------------

class StatusLivroUpdateView(View):
    template_name = "dashboard/home.html"

    def get(self, request, pk):
        status_item = get_object_or_404(tbl_status_livro, pk=pk)
        form = StatusLivroForm(instance=status_item)
        return render(request, self.template_name, {"form": form, "status_item": status_item})

    def post(self, request, pk):
        status_item = get_object_or_404(tbl_status_livro, pk=pk)
        form = StatusLivroForm(request.POST, instance=status_item)
        if form.is_valid():
            form.save()
            return redirect("status-list")
        return render(request, self.template_name, {"form": form, "status_item": status_item})


# DELETAR STATUS --------------------------------------------------------

class StatusLivroDeleteView(View):
    template_name = "biblioteca/dashboard/home.html"

    def get(self, request, pk):
        status_item = get_object_or_404(tbl_status_livro, pk=pk)
        return render(request, self.template_name, {"status_item": status_item})

    def post(self, request, pk):
        status_item = get_object_or_404(tbl_status_livro, pk=pk)
        status_item.delete()
        return redirect("status-list")
    
# LISTAR USUÁRIOS --------------------------------------------------------

class UsuarioListView(View):
    template_name = "biblioteca/usuario_list.html"

    def get(self, request):
        usuarios = tbl_usuario.objects.all()
        return render(request, self.template_name, {"usuarios": usuarios})

# CRIAR USUÁRIO ----------------------------------------------------------

class UsuarioCreateView(View):
    template_name = "biblioteca/usuario_form.html"

    def get(self, request):
        form = UsuarioForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("usuario-list")
        return render(request, self.template_name, {"form": form})


# EDITAR USUÁRIO ---------------------------------------------------------

class UsuarioUpdateView(View):
    template_name = "biblioteca/usuario_form.html"

    def get(self, request, pk):
        usuario = get_object_or_404(tbl_usuario, pk=pk)
        form = UsuarioForm(instance=usuario)
        return render(request, self.template_name, {"form": form, "usuario": usuario})

    def post(self, request, pk):
        usuario = get_object_or_404(tbl_usuario, pk=pk)
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect("usuario-list")
        return render(request, self.template_name, {"form": form, "usuario": usuario})


# DELETAR USUÁRIO ---------------------------------------------------------

class UsuarioDeleteView(View):
    template_name = "biblioteca/usuario_confirm_delete.html"

    def get(self, request, pk):
        usuario = get_object_or_404(tbl_usuario, pk=pk)
        return render(request, self.template_name, {"usuario": usuario})

    def post(self, request, pk):
        usuario = get_object_or_404(tbl_usuario, pk=pk)
        usuario.delete()
        return redirect("usuario-list")

# LISTAR MOTIVOS --------------------------------------------------------

class MotivoRemocaoListView(View):
    template_name = "biblioteca/motivo_list.html"

    def get(self, request):
        motivos = tbl_motivo_remocao.objects.all()
        return render(request, self.template_name, {"motivos": motivos})
    
    # CRIAR MOTIVO ----------------------------------------------------------

class MotivoRemocaoCreateView(View):
    template_name = "biblioteca/motivo_form.html"

    def get(self, request):
        form = MotivoRemocaoForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = MotivoRemocaoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("motivo-list")
        return render(request, self.template_name, {"form": form})


# EDITAR MOTIVO ---------------------------------------------------------

class MotivoRemocaoUpdateView(View):
    template_name = "biblioteca/motivo_form.html"

    def get(self, request, pk):
        motivo = get_object_or_404(tbl_motivo_remocao, pk=pk)
        form = MotivoRemocaoForm(instance=motivo)
        return render(request, self.template_name, {"form": form, "motivo": motivo})

    def post(self, request, pk):
        motivo = get_object_or_404(tbl_motivo_remocao, pk=pk)
        form = MotivoRemocaoForm(request.POST, instance=motivo)
        if form.is_valid():
            form.save()
            return redirect("motivo-list")
        return render(request, self.template_name, {"form": form, "motivo": motivo})


# EXCLUIR MOTIVO ---------------------------------------------------------

class MotivoRemocaoDeleteView(View):
    template_name = "biblioteca/motivo_confirm_delete.html"

    def get(self, request, pk):
        motivo = get_object_or_404(tbl_motivo_remocao, pk=pk)
        return render(request, self.template_name, {"motivo": motivo})

    def post(self, request, pk):
        motivo = get_object_or_404(tbl_motivo_remocao, pk=pk)
        motivo.delete()
        return redirect("motivo-list")