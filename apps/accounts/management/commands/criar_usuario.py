import getpass

from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError

from apps.accounts import services
from apps.accounts.models import User
from apps.accounts.roles import ROLE_CHOICES


class Command(BaseCommand):
    help = "Cria uma conta pelo terminal (ex.: o primeiro Administrador). A senha é pedida sem aparecer na tela."

    def add_arguments(self, parser):
        parser.add_argument("--email", required=True)
        parser.add_argument("--nome", required=True, help="Nome completo")
        parser.add_argument("--perfil", action="append", choices=ROLE_CHOICES, required=True,
                            help="Pode repetir para dar mais de um perfil")

    def handle(self, *args, email, nome, perfil, **options):
        email = User.objects.normalize_email(email).lower()
        if User.objects.filter(email__iexact=email).exists():
            raise CommandError("Já existe uma conta com este e-mail.")

        # Senha só pelo teclado: argumento de linha de comando fica no
        # histórico do terminal e na lista de processos.
        password = getpass.getpass("Senha: ")
        if password != getpass.getpass("Repita a senha: "):
            raise CommandError("As senhas não conferem.")
        try:
            password_validation.validate_password(password, User(email=email, full_name=nome))
        except ValidationError as error:
            raise CommandError(" ".join(error.messages))

        services.create_user(actor=None, email=email, full_name=nome, password=password, role_names=perfil)
        self.stdout.write(self.style.SUCCESS(f"Conta criada: {email} ({', '.join(perfil)})"))
