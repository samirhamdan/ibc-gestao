"""Quem pode e quem não pode: os quatro perfis contra cada tela protegida."""

from django.contrib.auth.models import Group, Permission
from django.test import TestCase
from django.urls import URLPattern, URLResolver, get_resolver, reverse

from apps.accounts.models import User
from apps.accounts.roles import ADMINISTRADOR, LIDER, MEMBRO, PASTOR, ROLE_PERMISSIONS, sync_roles
from apps.audit.models import AuditEvent

from .helpers import PASSWORD, make_user

# Páginas que precisam abrir sem login. Qualquer outra exige login.
PUBLIC_URL_NAMES = {
    "accounts:login",
    "accounts:password_reset",
    "accounts:password_reset_done",
    "accounts:password_reset_confirm",
    "accounts:password_reset_complete",
}


def _all_url_names(resolver=None, namespace=""):
    resolver = resolver or get_resolver()
    for pattern in resolver.url_patterns:
        if isinstance(pattern, URLResolver):
            ns = pattern.namespace or ""
            yield from _all_url_names(pattern, f"{namespace}{ns}:" if ns else namespace)
        elif isinstance(pattern, URLPattern) and pattern.name:
            yield f"{namespace}{pattern.name}", pattern


def _sample_url(name, pattern):
    kwargs = {}
    for key in pattern.pattern.converters:
        kwargs[key] = 1 if key == "pk" else "x"
    return reverse(name, kwargs=kwargs)


class RolesTests(TestCase):
    def test_os_quatro_perfis_existem_com_as_permissoes_definidas(self):
        for name, expected in ROLE_PERMISSIONS.items():
            group = Group.objects.get(name=name)
            actual = {f"{p.content_type.app_label}.{p.codename}" for p in group.permissions.all()}
            self.assertEqual(actual, expected, name)

    def test_sincronizar_remove_permissao_acrescentada_a_mao(self):
        group = Group.objects.get(name=MEMBRO)
        group.permissions.add(Permission.objects.get(codename="change_user"))
        sync_roles()
        self.assertFalse(group.permissions.exists())

    def test_superusuario_nao_pode_ser_criado(self):
        with self.assertRaises(NotImplementedError):
            User.objects.create_superuser("x@exemplo.test", "X", "Senha-de-teste-123")


class LoginRequiredTests(TestCase):
    def test_toda_pagina_nao_publica_exige_login(self):
        checked = 0
        for name, pattern in _all_url_names():
            if name in PUBLIC_URL_NAMES:
                continue
            url = _sample_url(name, pattern)
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302, url)
            self.assertTrue(response["Location"].startswith(reverse("accounts:login")), url)
            checked += 1
        self.assertGreater(checked, 5)

    def test_paginas_publicas_abrem_sem_login(self):
        for name in ["accounts:login", "accounts:password_reset", "accounts:password_reset_done"]:
            self.assertEqual(self.client.get(reverse(name)).status_code, 200, name)


class UserManagementAccessTests(TestCase):
    """Só o Administrador gerencia usuários. Os outros recebem 403, mesmo
    digitando o endereço direto."""

    @classmethod
    def setUpTestData(cls):
        cls.admin = make_user(ADMINISTRADOR)
        cls.others = [make_user(PASTOR), make_user(LIDER), make_user(MEMBRO), make_user(None)]
        cls.target = make_user(MEMBRO, email="alvo@exemplo.test")

    def urls(self):
        return [
            reverse("accounts:user_list"),
            reverse("accounts:user_create"),
            reverse("accounts:user_edit", args=[self.target.pk]),
            reverse("accounts:user_set_password", args=[self.target.pk]),
        ]

    def test_administrador_acessa(self):
        self.client.force_login(self.admin)
        for url in self.urls():
            self.assertEqual(self.client.get(url).status_code, 200, url)

    def test_demais_perfis_recebem_403_no_get_e_no_post(self):
        for user in self.others:
            self.client.force_login(user)
            for url in self.urls():
                self.assertEqual(self.client.get(url).status_code, 403, f"{user.email} GET {url}")
                self.assertEqual(self.client.post(url, {}).status_code, 403, f"{user.email} POST {url}")

    def test_todos_os_perfis_acessam_a_propria_conta(self):
        for user in [self.admin, *self.others]:
            self.client.force_login(user)
            self.assertEqual(self.client.get(reverse("accounts:home")).status_code, 200)

    def test_menu_so_mostra_usuarios_para_quem_pode(self):
        self.client.force_login(self.admin)
        self.assertContains(self.client.get(reverse("accounts:home")), reverse("accounts:user_list"))
        self.client.force_login(self.others[2])
        self.assertNotContains(self.client.get(reverse("accounts:home")), reverse("accounts:user_list"))

    def test_id_inexistente_responde_404_para_administrador(self):
        self.client.force_login(self.admin)
        self.assertEqual(self.client.get(reverse("accounts:user_edit", args=[999999])).status_code, 404)


class PrivilegeEscalationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = make_user(ADMINISTRADOR)
        cls.member = make_user(MEMBRO)

    def test_membro_nao_se_promove_por_requisicao_direta(self):
        self.client.force_login(self.member)
        response = self.client.post(
            reverse("accounts:user_edit", args=[self.member.pk]),
            {"full_name": "Eu", "email": self.member.email, "is_active": "on", "roles": [ADMINISTRADOR]},
        )
        self.assertEqual(response.status_code, 403)
        self.member.refresh_from_db()
        self.assertEqual(self.member.role_names, [MEMBRO])
        self.assertFalse(AuditEvent.objects.exists())

    def test_membro_nao_cria_administrador(self):
        self.client.force_login(self.member)
        response = self.client.post(
            reverse("accounts:user_create"),
            {"full_name": "Intruso", "email": "intruso@exemplo.test", "roles": [ADMINISTRADOR],
             "password1": PASSWORD, "password2": PASSWORD},
        )
        self.assertEqual(response.status_code, 403)
        self.assertFalse(User.objects.filter(email="intruso@exemplo.test").exists())

    def test_perfil_inexistente_e_rejeitado(self):
        self.client.force_login(self.admin)
        response = self.client.post(
            reverse("accounts:user_edit", args=[self.member.pk]),
            {"full_name": "X", "email": self.member.email, "is_active": "on", "roles": ["Superusuário"]},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)
        self.member.refresh_from_db()
        self.assertEqual(self.member.role_names, [MEMBRO])

    def test_campos_de_superusuario_sao_ignorados(self):
        self.client.force_login(self.admin)
        self.client.post(
            reverse("accounts:user_edit", args=[self.member.pk]),
            {"full_name": "X", "email": self.member.email, "is_active": "on", "roles": [MEMBRO],
             "is_superuser": "on", "is_staff": "on"},
        )
        self.member.refresh_from_db()
        self.assertFalse(self.member.is_superuser)

    def test_administrador_nao_se_desativa(self):
        self.client.force_login(self.admin)
        response = self.client.post(
            reverse("accounts:user_edit", args=[self.admin.pk]),
            {"full_name": self.admin.full_name, "email": self.admin.email, "roles": [ADMINISTRADOR]},
        )
        self.assertContains(response, "Você não pode desativar a sua própria conta.")
        self.admin.refresh_from_db()
        self.assertTrue(self.admin.is_active)

    def test_administrador_nao_remove_o_proprio_perfil(self):
        self.client.force_login(self.admin)
        response = self.client.post(
            reverse("accounts:user_edit", args=[self.admin.pk]),
            {"full_name": self.admin.full_name, "email": self.admin.email, "is_active": "on", "roles": [PASTOR]},
        )
        self.assertContains(response, "Você não pode remover o seu próprio perfil de Administrador.")
        self.admin.refresh_from_db()
        self.assertEqual(self.admin.role_names, [ADMINISTRADOR])

    def test_administrador_nao_tem_permissoes_alem_das_definidas(self):
        # Administrador gerencia contas, mas não é superusuário: não herda
        # acesso a tudo (ex.: registros pastorais das próximas sprints).
        self.assertFalse(self.admin.is_superuser)
        self.assertFalse(self.admin.has_perm("accounts.delete_user"))


class DeactivatedUserTests(TestCase):
    def test_usuario_desativado_nao_entra(self):
        user = make_user(MEMBRO, active=False)
        response = self.client.post(reverse("accounts:login"), {"username": user.email, "password": PASSWORD})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "E-mail ou senha incorretos.")
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_desativar_derruba_a_sessao_aberta(self):
        admin = make_user(ADMINISTRADOR)
        member = make_user(MEMBRO)
        member_client = self.client_class()
        member_client.force_login(member)
        self.assertEqual(member_client.get(reverse("accounts:home")).status_code, 200)

        self.client.force_login(admin)
        self.client.post(
            reverse("accounts:user_edit", args=[member.pk]),
            {"full_name": member.full_name, "email": member.email, "roles": [MEMBRO]},
        )
        member.refresh_from_db()
        self.assertFalse(member.is_active)

        response = member_client.get(reverse("accounts:home"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response["Location"].startswith(reverse("accounts:login")))
