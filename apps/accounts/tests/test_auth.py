"""Login, logout, senha provisória e recuperação de senha."""

import re
from io import StringIO
from unittest import mock

from django.core import mail
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import User
from apps.accounts.roles import ADMINISTRADOR, MEMBRO
from apps.audit.models import AuditEvent

from .helpers import PASSWORD, make_user

NEW_PASSWORD = "Outra-senha-de-teste-456"


class LoginTests(TestCase):
    def test_login_com_email_em_maiusculas(self):
        user = make_user(MEMBRO)
        response = self.client.post(reverse("accounts:login"), {"username": user.email.upper(), "password": PASSWORD})
        self.assertRedirects(response, reverse("accounts:home"))

    def test_erro_nao_revela_se_a_conta_existe(self):
        user = make_user(MEMBRO)
        wrong_password = self.client.post(reverse("accounts:login"), {"username": user.email, "password": "errada-123"})
        unknown = self.client.post(reverse("accounts:login"), {"username": "ninguem@exemplo.test", "password": "errada-123"})
        self.assertEqual(wrong_password.context["form"].non_field_errors(), unknown.context["form"].non_field_errors())
        self.assertContains(unknown, "E-mail ou senha incorretos.")

    def test_logout_so_por_post(self):
        self.client.force_login(make_user(MEMBRO))
        self.assertEqual(self.client.get(reverse("accounts:logout")).status_code, 405)
        self.client.post(reverse("accounts:logout"))
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_redirecionamento_externo_apos_login_e_ignorado(self):
        user = make_user(MEMBRO)
        response = self.client.post(
            reverse("accounts:login") + "?next=https://site-malicioso.test/",
            {"username": user.email, "password": PASSWORD, "next": "https://site-malicioso.test/"},
        )
        self.assertRedirects(response, reverse("accounts:home"))


class ProvisionalPasswordTests(TestCase):
    def test_senha_provisoria_obriga_troca_antes_de_tudo(self):
        user = make_user(MEMBRO, must_change_password=True)
        self.client.force_login(user)
        self.assertRedirects(self.client.get(reverse("accounts:home")), reverse("accounts:password_change"))

        response = self.client.post(
            reverse("accounts:password_change"),
            {"old_password": PASSWORD, "new_password1": NEW_PASSWORD, "new_password2": NEW_PASSWORD},
        )
        self.assertRedirects(response, reverse("accounts:password_change_done"))
        user.refresh_from_db()
        self.assertFalse(user.must_change_password)
        self.assertEqual(self.client.get(reverse("accounts:home")).status_code, 200)

    def test_usuario_criado_pelo_administrador_tem_senha_provisoria(self):
        self.client.force_login(make_user(ADMINISTRADOR))
        response = self.client.post(
            reverse("accounts:user_create"),
            {"full_name": "Pessoa Nova", "email": "Nova@Exemplo.test", "roles": [MEMBRO],
             "password1": PASSWORD, "password2": PASSWORD},
        )
        self.assertRedirects(response, reverse("accounts:user_list"))
        user = User.objects.get(email="nova@exemplo.test")
        self.assertTrue(user.must_change_password)
        self.assertEqual(user.role_names, [MEMBRO])

    def test_senha_fraca_e_recusada(self):
        self.client.force_login(make_user(ADMINISTRADOR))
        response = self.client.post(
            reverse("accounts:user_create"),
            {"full_name": "Pessoa Nova", "email": "nova@exemplo.test", "roles": [MEMBRO],
             "password1": "12345678", "password2": "12345678"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("password1", response.context["form"].errors)
        self.assertFalse(User.objects.filter(email="nova@exemplo.test").exists())

    def test_email_repetido_com_outra_caixa_e_recusado(self):
        make_user(MEMBRO, email="repetido@exemplo.test")
        self.client.force_login(make_user(ADMINISTRADOR))
        response = self.client.post(
            reverse("accounts:user_create"),
            {"full_name": "Outra", "email": "REPETIDO@exemplo.test", "roles": [],
             "password1": PASSWORD, "password2": PASSWORD},
        )
        self.assertContains(response, "Já existe uma conta com este e-mail.")

    def test_administrador_define_senha_provisoria(self):
        admin = make_user(ADMINISTRADOR)
        member = make_user(MEMBRO)
        self.client.force_login(admin)
        self.client.post(
            reverse("accounts:user_set_password", args=[member.pk]),
            {"password1": NEW_PASSWORD, "password2": NEW_PASSWORD},
        )
        member.refresh_from_db()
        self.assertTrue(member.check_password(NEW_PASSWORD))
        self.assertTrue(member.must_change_password)
        event = AuditEvent.objects.get(action=AuditEvent.Action.USER_PASSWORD_SET_BY_ADMIN)
        self.assertNotIn(NEW_PASSWORD, str(event.changes))


class PasswordResetTests(TestCase):
    def test_mesma_resposta_para_email_cadastrado_ou_nao(self):
        user = make_user(MEMBRO)
        known = self.client.post(reverse("accounts:password_reset"), {"email": user.email})
        unknown = self.client.post(reverse("accounts:password_reset"), {"email": "ninguem@exemplo.test"})
        self.assertRedirects(known, reverse("accounts:password_reset_done"))
        self.assertRedirects(unknown, reverse("accounts:password_reset_done"))
        self.assertEqual(len(mail.outbox), 1)

    def test_conta_desativada_nao_recebe_link(self):
        user = make_user(MEMBRO, active=False)
        self.client.post(reverse("accounts:password_reset"), {"email": user.email})
        self.assertEqual(len(mail.outbox), 0)

    def test_fluxo_completo_e_link_de_uso_unico(self):
        user = make_user(MEMBRO, must_change_password=True)
        self.client.post(reverse("accounts:password_reset"), {"email": user.email})
        link = re.search(r"https?://[^/]+(/senha/redefinir/\S+)", mail.outbox[0].body).group(1)

        response = self.client.get(link, follow=True)
        form_url = response.redirect_chain[-1][0]
        response = self.client.post(form_url, {"new_password1": NEW_PASSWORD, "new_password2": NEW_PASSWORD})
        self.assertRedirects(response, reverse("accounts:password_reset_complete"))

        user.refresh_from_db()
        self.assertTrue(user.check_password(NEW_PASSWORD))
        self.assertFalse(user.must_change_password)

        reused = self.client.get(link, follow=True)
        self.assertContains(reused, "Link inválido")


class CreateUserCommandTests(TestCase):
    def run_command(self, passwords, **kwargs):
        with mock.patch("getpass.getpass", side_effect=passwords):
            call_command("criar_usuario", stdout=StringIO(), **kwargs)

    def test_cria_o_primeiro_administrador(self):
        self.run_command([PASSWORD, PASSWORD], email="Admin@Exemplo.test", nome="Admin Fictício", perfil=[ADMINISTRADOR])
        user = User.objects.get(email="admin@exemplo.test")
        self.assertEqual(user.role_names, [ADMINISTRADOR])
        self.assertFalse(user.must_change_password)
        self.assertTrue(AuditEvent.objects.filter(action=AuditEvent.Action.USER_CREATED, actor=None).exists())

    def test_recusa_senha_fraca(self):
        with self.assertRaises(CommandError):
            self.run_command(["12345678", "12345678"], email="a@exemplo.test", nome="A", perfil=[MEMBRO])
        self.assertFalse(User.objects.exists())
