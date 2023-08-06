from __future__ import unicode_literals

import inspect

from django_user_role.role import RolesManager, get_user_roles


def has_permission(user, permission_name):
    if user and user.is_superuser:
        return True

    return user.has_perm(permission_name)


def has_role(user, roles):
    """
    todo 有可能需要判断的是同时具有多个权限
    """
    if user and user.is_superuser:
        return True

    if not isinstance(roles, list):
        roles = [roles]

    normalized_roles = []
    for role in roles:
        if not inspect.isclass(role):
            role = RolesManager.retrieve_role(role)

        normalized_roles.append(role)

    user_roles = get_user_roles(user)

    return any([role in user_roles for role in normalized_roles])
