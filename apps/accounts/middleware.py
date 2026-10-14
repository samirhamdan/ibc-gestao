from django.shortcuts import redirect
from django.urls import reverse


class ForcePasswordChangeMiddleware:
    """Enquanto a senha for provisória (criada pelo administrador), a pessoa
    só consegue trocar a senha ou sair."""

    allowed_url_names = ("accounts:password_change", "accounts:password_change_done", "accounts:logout")

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, "user", None)
        if user is not None and user.is_authenticated and user.must_change_password:
            allowed = {reverse(name) for name in self.allowed_url_names}
            if request.path not in allowed:
                return redirect("accounts:password_change")
        return self.get_response(request)
