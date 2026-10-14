from django.conf import settings
from django.db import models


class AuditEvent(models.Model):
    """Registro de uma ação relevante. Só se cria; nunca se altera nem apaga.

    `changes` guarda os nomes dos campos alterados e, quando o valor não é
    sensível (ex.: perfis, ativo/inativo), o antes e o depois. Nunca guardar
    senha, token ou dado pessoal sensível aqui.
    """

    class Action(models.TextChoices):
        USER_CREATED = "user.created", "Usuário criado"
        USER_UPDATED = "user.updated", "Usuário alterado"
        USER_ROLES_CHANGED = "user.roles_changed", "Perfis alterados"
        USER_ACTIVATED = "user.activated", "Usuário ativado"
        USER_DEACTIVATED = "user.deactivated", "Usuário desativado"
        USER_PASSWORD_SET_BY_ADMIN = "user.password_set_by_admin", "Senha definida pelo administrador"

    created_at = models.DateTimeField("data/hora", auto_now_add=True, db_index=True)
    # PROTECT: apagar um usuário não pode apagar o rastro do que ele fez.
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="autor",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="+",
    )
    action = models.CharField("ação", max_length=64, choices=Action.choices)
    target_type = models.CharField("tipo do objeto", max_length=64)
    target_id = models.CharField("id do objeto", max_length=64)
    changes = models.JSONField("alterações", default=dict, blank=True)

    class Meta:
        verbose_name = "evento de auditoria"
        verbose_name_plural = "eventos de auditoria"
        ordering = ["-created_at", "-id"]
        indexes = [models.Index(fields=["target_type", "target_id"])]
        default_permissions = ("view",)

    def __str__(self):
        return f"{self.created_at:%Y-%m-%d %H:%M} {self.action} {self.target_type}#{self.target_id}"

    def save(self, *args, **kwargs):
        if self.pk is not None:
            raise PermissionError("Eventos de auditoria não podem ser alterados.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise PermissionError("Eventos de auditoria não podem ser apagados.")
