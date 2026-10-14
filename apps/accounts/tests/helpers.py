from django.contrib.auth.models import Group

from apps.accounts.models import User

# Dados fictícios. Nunca usar dados reais de membros nos testes.
PASSWORD = "Senha-de-teste-123"


def make_user(role=None, email=None, active=True, must_change_password=False):
    slug = (role or "sem-perfil").lower().replace("í", "i")
    user = User.objects.create_user(
        email=email or f"{slug}@exemplo.test",
        full_name=f"Pessoa Fictícia {role or 'Sem Perfil'}",
        password=PASSWORD,
        is_active=active,
        must_change_password=must_change_password,
    )
    if role:
        user.groups.add(Group.objects.get(name=role))
    return user
