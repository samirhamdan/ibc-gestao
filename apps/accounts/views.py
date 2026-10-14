from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods

from . import services
from .forms import AdminSetPasswordForm, LoginForm, UserCreateForm, UserUpdateForm
from .models import User


class LoginView(auth_views.LoginView):
    form_class = LoginForm
    redirect_authenticated_user = True


class PasswordChangeView(auth_views.PasswordChangeView):
    success_url = reverse_lazy("accounts:password_change_done")

    def form_valid(self, form):
        response = super().form_valid(form)
        services.password_changed_by_owner(self.request.user)
        return response


class PasswordResetView(auth_views.PasswordResetView):
    success_url = reverse_lazy("accounts:password_reset_done")


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    success_url = reverse_lazy("accounts:password_reset_complete")

    def form_valid(self, form):
        response = super().form_valid(form)
        services.password_changed_by_owner(form.user)
        return response


def home(request):
    return render(request, "accounts/home.html")


@permission_required("accounts.view_user", raise_exception=True)
def user_list(request):
    users = User.objects.prefetch_related("groups").order_by("full_name")
    page = Paginator(users, 25).get_page(request.GET.get("pagina"))
    return render(request, "accounts/user_list.html", {"page": page})


@permission_required("accounts.add_user", raise_exception=True)
@require_http_methods(["GET", "POST"])
def user_create(request):
    form = UserCreateForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data
        try:
            services.create_user(
                actor=request.user,
                email=data["email"],
                full_name=data["full_name"],
                password=data["password1"],
                role_names=data["roles"],
            )
        except ValidationError as error:
            form.add_error(None, error)
        else:
            messages.success(request, "Usuário criado.")
            return redirect("accounts:user_list")
    return render(request, "accounts/user_form.html", {"form": form, "title": "Novo usuário"})


@permission_required("accounts.change_user", raise_exception=True)
@require_http_methods(["GET", "POST"])
def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    form = UserUpdateForm(request.POST or None, user=user)
    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data
        try:
            services.update_user(
                actor=request.user,
                user=user,
                full_name=data["full_name"],
                email=data["email"],
                is_active=data["is_active"],
                role_names=data["roles"],
            )
        except ValidationError as error:
            form.add_error(None, error)
        else:
            messages.success(request, "Usuário atualizado.")
            return redirect("accounts:user_list")
    return render(
        request,
        "accounts/user_form.html",
        {"form": form, "title": f"Editar usuário: {user.full_name}", "edited_user": user},
    )


@permission_required("accounts.change_user", raise_exception=True)
@require_http_methods(["GET", "POST"])
def user_set_password(request, pk):
    user = get_object_or_404(User, pk=pk)
    form = AdminSetPasswordForm(request.POST or None, user=user)
    if request.method == "POST" and form.is_valid():
        services.set_password_by_admin(actor=request.user, user=user, password=form.cleaned_data["password1"])
        messages.success(request, "Senha provisória definida. A pessoa deverá trocá-la no próximo acesso.")
        return redirect("accounts:user_list")
    return render(
        request,
        "accounts/user_form.html",
        {"form": form, "title": f"Definir senha provisória: {user.full_name}"},
    )
