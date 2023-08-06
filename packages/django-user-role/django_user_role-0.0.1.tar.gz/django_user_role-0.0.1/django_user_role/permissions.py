from django_user_role.exceptions import (
    RolePermissionScopeException, CheckerNotRegistered)
from django_user_role.role import get_user_roles, get_or_create_permission


class PermissionsManager(object):
    _checkers = {}

    @classmethod
    def register_checker(cls, name, function):
        cls._checkers[name] = function

    @classmethod
    def get_checkers(cls):
        return cls._checkers

    @classmethod
    def retrieve_checker(cls, checker_name):
        if checker_name in cls._checkers:
            return cls._checkers[checker_name]

        raise CheckerNotRegistered('Checker with name %s was not registered' % checker_name)


def get_permission(permission_name):
    permission, created = get_or_create_permission(permission_name)

    return permission


def grant_permission(user, permission_name):
    roles = get_user_roles(user)

    for role in roles:
        if permission_name in role.permission_names_list():
            permission = get_permission(permission_name)
            user.user_permissions.add(permission)
            return

    raise RolePermissionScopeException(
        "This permission isn't in the scope of "
        "any of this user's roles.")


def revoke_permission(user, permission_name):
    roles = get_user_roles(user)

    for role in roles:
        if permission_name in role.permission_names_list():
            permission = get_permission(permission_name)
            user.user_permissions.remove(permission)
            return

    raise RolePermissionScopeException(
        "This permission isn't in the scope of "
        "any of this user's roles.")
