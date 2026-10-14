from django.apps import AppConfig
from django.db.models.signals import post_migrate


class AccountsConfig(AppConfig):
    name = "apps.accounts"
    label = "accounts"
    verbose_name = "Contas e perfis"

    def ready(self):
        from .roles import sync_roles_after_migrate

        post_migrate.connect(sync_roles_after_migrate, sender=self)
