"""Os perfis do sistema e o que cada um pode fazer.

Este arquivo é a fonte da verdade: a cada `migrate`, os grupos do banco são
ajustados para ficar exatamente como está aqui (inclusive removendo
permissões que alguém tenha acrescentado à mão). Mudar uma permissão de
perfil é mudar este arquivo, com revisão e commit.
"""

from django.apps import apps as global_apps
from django.contrib.auth.management import create_permissions

ADMINISTRADOR = "Administrador"
PASTOR = "Pastor"
LIDER = "Líder"
MEMBRO = "Membro"

ROLE_CHOICES = [ADMINISTRADOR, PASTOR, LIDER, MEMBRO]

# Permissões no formato "app_label.codename".
# Pastor, Líder e Membro ainda não têm permissões: os dados que eles vão
# consultar (pessoas, membresia, recadastramento) chegam a partir da Sprint 3.
# Por enquanto eles só acessam a própria conta.
ROLE_PERMISSIONS = {
    ADMINISTRADOR: {
        "accounts.view_user",
        "accounts.add_user",
        "accounts.change_user",
        "accounts.assign_roles",
        "audit.view_auditevent",
    },
    PASTOR: set(),
    LIDER: set(),
    MEMBRO: set(),
}


def sync_roles(apps=global_apps, using="default"):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")

    wanted = {perm for perms in ROLE_PERMISSIONS.values() for perm in perms}
    found = {}
    for perm in Permission.objects.using(using).select_related("content_type"):
        key = f"{perm.content_type.app_label}.{perm.codename}"
        if key in wanted:
            found[key] = perm
    missing = wanted - found.keys()
    if missing:
        raise RuntimeError(f"Permissões inexistentes em roles.py: {sorted(missing)}")

    for name, perms in ROLE_PERMISSIONS.items():
        group, _ = Group.objects.using(using).get_or_create(name=name)
        group.permissions.set([found[p] for p in perms])


def sync_roles_after_migrate(sender, using="default", apps=global_apps, **kwargs):
    # As permissões de cada app são criadas no post_migrate do próprio app,
    # e a ordem não é garantida. Criá-las aqui antes evita depender disso.
    for app_config in global_apps.get_app_configs():
        create_permissions(app_config, verbosity=0, using=using)
    sync_roles(using=using)
