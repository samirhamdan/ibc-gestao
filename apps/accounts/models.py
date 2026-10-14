from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.db.models.functions import Lower
from django.utils import timezone


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, full_name, password=None, **extra_fields):
        if not email:
            raise ValueError("O e-mail é obrigatório.")
        user = self.model(email=self.normalize_email(email).lower(), full_name=full_name, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, *args, **kwargs):
        # Superusuário ignora todas as permissões, inclusive as de registros
        # pastorais. O CLAUDE.md proíbe acesso irrestrito por padrão.
        raise NotImplementedError(
            "Superusuário não é usado neste sistema. "
            "Use: python manage.py criar_usuario --perfil Administrador"
        )

    def get_by_natural_key(self, email):
        return self.get(email__iexact=email)


class User(AbstractBaseUser, PermissionsMixin):
    """Conta de acesso. Os perfis são os grupos do Django (ver roles.py).

    A conta é separada do cadastro da pessoa (Sprint 3): nem toda pessoa terá
    login, e os dados eclesiásticos não ficam aqui.
    """

    email = models.EmailField("e-mail", max_length=254, unique=True)
    full_name = models.CharField("nome completo", max_length=150)
    is_active = models.BooleanField(
        "ativo",
        default=True,
        help_text="Desmarque para bloquear o acesso sem apagar a conta.",
    )
    must_change_password = models.BooleanField(
        "deve trocar a senha",
        default=False,
        help_text="Obriga a pessoa a criar uma senha própria no próximo acesso.",
    )
    date_joined = models.DateTimeField("criado em", default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    class Meta:
        verbose_name = "usuário"
        verbose_name_plural = "usuários"
        ordering = ["full_name"]
        constraints = [
            # Fulano@x.com e fulano@x.com são a mesma conta. O código já grava
            # em minúsculas; a restrição garante isso também no banco.
            models.UniqueConstraint(Lower("email"), name="accounts_user_email_ci_unique"),
        ]
        permissions = [
            ("assign_roles", "Pode atribuir perfis de acesso"),
        ]

    def __str__(self):
        return self.full_name

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email).lower()

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.full_name.split(" ")[0]

    @property
    def role_names(self):
        return sorted(group.name for group in self.groups.all())
