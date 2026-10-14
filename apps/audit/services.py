from .models import AuditEvent


def record(actor, action, target, changes=None):
    """Registra uma ação. Chamar dentro da mesma transação da ação auditada,
    para que não exista ação sem registro nem registro de ação desfeita."""
    return AuditEvent.objects.create(
        actor=actor if actor is not None and actor.is_authenticated else None,
        action=action,
        target_type=target._meta.label_lower,
        target_id=str(target.pk),
        changes=changes or {},
    )
