"""Regras de negócio de contas e perfis. Views e comandos só chamam daqui."""

from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction

from apps.audit.models import AuditEvent
from apps.audit.services import record

from .models import User
from .roles import ADMINISTRADOR, ROLE_CHOICES


def _groups_for(role_names):
    unknown = set(role_names) - set(ROLE_CHOICES)
    if unknown:
        raise ValidationError(f"Perfil inválido: {', '.join(sorted(unknown))}")
    return list(Group.objects.filter(name__in=role_names))


def _check_can_assign_roles(actor):
    # actor=None é o comando de terminal, usado por quem já tem acesso ao
    # servidor (ex.: criar o primeiro administrador).
    if actor is not None and not actor.has_perm("accounts.assign_roles"):
        raise PermissionDenied


@transaction.atomic
def create_user(*, actor, email, full_name, password, role_names):
    if actor is not None and not actor.has_perm("accounts.add_user"):
        raise PermissionDenied
    _check_can_assign_roles(actor)
    groups = _groups_for(role_names)

    user = User.objects.create_user(
        email=email,
        full_name=full_name,
        password=password,
        # Senha criada por outra pessoa é provisória.
        must_change_password=actor is not None,
    )
    user.groups.set(groups)
    record(actor, AuditEvent.Action.USER_CREATED, user, {"roles": sorted(role_names)})
    return user


@transaction.atomic
def update_user(*, actor, user, full_name, email, is_active, role_names):
    if not actor.has_perm("accounts.change_user"):
        raise PermissionDenied

    old_roles = set(user.role_names)
    new_roles = set(role_names)
    if new_roles != old_roles:
        _check_can_assign_roles(actor)
    groups = _groups_for(new_roles)

    if user.pk == actor.pk:
        # Evita que o sistema fique sem ninguém capaz de administrá-lo.
        if not is_active:
            raise ValidationError("Você não pode desativar a sua própria conta.")
        if ADMINISTRADOR in old_roles and ADMINISTRADOR not in new_roles:
            raise ValidationError("Você não pode remover o seu próprio perfil de Administrador.")

    changed_fields = []
    if user.full_name != full_name:
        user.full_name = full_name
        changed_fields.append("full_name")
    email = User.objects.normalize_email(email).lower()
    if user.email != email:
        user.email = email
        changed_fields.append("email")
    was_active = user.is_active
    user.is_active = is_active
    user.save()

    if changed_fields:
        record(actor, AuditEvent.Action.USER_UPDATED, user, {"fields": changed_fields})
    if was_active != is_active:
        action = AuditEvent.Action.USER_ACTIVATED if is_active else AuditEvent.Action.USER_DEACTIVATED
        record(actor, action, user)
    if new_roles != old_roles:
        user.groups.set(groups)
        record(
            actor,
            AuditEvent.Action.USER_ROLES_CHANGED,
            user,
            {"before": sorted(old_roles), "after": sorted(new_roles)},
        )
    return user


@transaction.atomic
def set_password_by_admin(*, actor, user, password):
    if not actor.has_perm("accounts.change_user"):
        raise PermissionDenied
    user.set_password(password)
    user.must_change_password = True
    user.save(update_fields=["password", "must_change_password"])
    record(actor, AuditEvent.Action.USER_PASSWORD_SET_BY_ADMIN, user)
    return user


def password_changed_by_owner(user):
    if user.must_change_password:
        user.must_change_password = False
        user.save(update_fields=["must_change_password"])
