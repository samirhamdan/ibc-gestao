from io import StringIO

from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from apps.accounts.roles import ADMINISTRADOR, MEMBRO, PASTOR
from apps.audit.models import AuditEvent

from .helpers import make_user


class AccessChangesAreAuditedTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = make_user(ADMINISTRADOR)
        cls.member = make_user(MEMBRO)

    def edit_member(self, **overrides):
        data = {"full_name": self.member.full_name, "email": self.member.email, "is_active": "on", "roles": [MEMBRO]}
        data.update(overrides)
        self.client.force_login(self.admin)
        return self.client.post(reverse("accounts:user_edit", args=[self.member.pk]), data)

    def test_mudanca_de_perfil_registra_antes_e_depois(self):
        self.edit_member(roles=[MEMBRO, PASTOR])
        event = AuditEvent.objects.get(action=AuditEvent.Action.USER_ROLES_CHANGED)
        self.assertEqual(event.actor, self.admin)
        self.assertEqual(event.target_id, str(self.member.pk))
        self.assertEqual(event.changes, {"before": [MEMBRO], "after": [MEMBRO, PASTOR]})

    def test_desativacao_e_registrada(self):
        self.edit_member(is_active="")
        self.assertTrue(AuditEvent.objects.filter(action=AuditEvent.Action.USER_DEACTIVATED).exists())

    def test_alteracao_de_dados_registra_so_os_nomes_dos_campos(self):
        self.edit_member(email="novo-email@exemplo.test")
        event = AuditEvent.objects.get(action=AuditEvent.Action.USER_UPDATED)
        self.assertEqual(event.changes, {"fields": ["email"]})
        self.assertNotIn("novo-email", str(event.changes))

    def test_salvar_sem_mudar_nada_nao_gera_registro(self):
        self.edit_member()
        self.assertFalse(AuditEvent.objects.exists())

    def test_registro_de_auditoria_nao_pode_ser_alterado_nem_apagado(self):
        self.edit_member(roles=[PASTOR])
        event = AuditEvent.objects.get()
        event.action = AuditEvent.Action.USER_CREATED
        with self.assertRaises(PermissionError):
            event.save()
        with self.assertRaises(PermissionError):
            event.delete()


class MigrationsTests(TestCase):
    def test_nao_ha_migration_esquecida(self):
        # Falha se alguém mudou um modelo e não gerou a migration.
        call_command("makemigrations", "--check", "--dry-run", stdout=StringIO())
