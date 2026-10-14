from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm

from .models import User
from .roles import ROLE_CHOICES


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="E-mail", widget=forms.EmailInput(attrs={"autofocus": True, "autocomplete": "email"}))

    error_messages = {
        # Mesma mensagem para e-mail inexistente, senha errada e conta
        # desativada: a tela não pode revelar quem tem conta no sistema.
        "invalid_login": "E-mail ou senha incorretos.",
        "inactive": "E-mail ou senha incorretos.",
    }


class RolesField(forms.MultipleChoiceField):
    def __init__(self, **kwargs):
        super().__init__(
            label="Perfis",
            choices=[(name, name) for name in ROLE_CHOICES],
            widget=forms.CheckboxSelectMultiple,
            required=False,
            **kwargs,
        )


class _EmailUniqueMixin:
    def clean_email(self):
        email = User.objects.normalize_email(self.cleaned_data["email"]).lower()
        others = User.objects.filter(email__iexact=email)
        if getattr(self, "instance_pk", None):
            others = others.exclude(pk=self.instance_pk)
        if others.exists():
            raise forms.ValidationError("Já existe uma conta com este e-mail.")
        return email


class UserCreateForm(_EmailUniqueMixin, forms.Form):
    full_name = forms.CharField(label="Nome completo", max_length=150)
    email = forms.EmailField(label="E-mail", max_length=254)
    roles = RolesField()
    password1 = forms.CharField(
        label="Senha provisória",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text="A pessoa será obrigada a trocá-la no primeiro acesso.",
    )
    password2 = forms.CharField(
        label="Confirme a senha provisória",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )

    def clean(self):
        cleaned = super().clean()
        p1, p2 = cleaned.get("password1"), cleaned.get("password2")
        if p1 and p2 and p1 != p2:
            self.add_error("password2", "As senhas não conferem.")
        elif p1:
            candidate = User(email=cleaned.get("email", ""), full_name=cleaned.get("full_name", ""))
            try:
                password_validation.validate_password(p1, candidate)
            except forms.ValidationError as error:
                self.add_error("password1", error)
        return cleaned


class UserUpdateForm(_EmailUniqueMixin, forms.Form):
    full_name = forms.CharField(label="Nome completo", max_length=150)
    email = forms.EmailField(label="E-mail", max_length=254)
    is_active = forms.BooleanField(
        label="Conta ativa",
        required=False,
        help_text="Desmarque para bloquear o acesso. A conta não é apagada.",
    )
    roles = RolesField()

    def __init__(self, *args, user, **kwargs):
        self.instance_pk = user.pk
        kwargs.setdefault(
            "initial",
            {"full_name": user.full_name, "email": user.email, "is_active": user.is_active, "roles": user.role_names},
        )
        super().__init__(*args, **kwargs)


class AdminSetPasswordForm(forms.Form):
    password1 = forms.CharField(
        label="Nova senha provisória",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text="A pessoa será obrigada a trocá-la no próximo acesso.",
    )
    password2 = forms.CharField(
        label="Confirme a nova senha provisória",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )

    def __init__(self, *args, user, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned = super().clean()
        p1, p2 = cleaned.get("password1"), cleaned.get("password2")
        if p1 and p2 and p1 != p2:
            self.add_error("password2", "As senhas não conferem.")
        elif p1:
            try:
                password_validation.validate_password(p1, self.user)
            except forms.ValidationError as error:
                self.add_error("password1", error)
        return cleaned
