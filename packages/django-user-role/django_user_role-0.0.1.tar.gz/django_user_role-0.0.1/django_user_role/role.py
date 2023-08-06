import inspect
import logging
from six import add_metaclass
from django.db import transaction
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django_user_role.models import Role, PermissionRefCount
from django_user_role.utils import camel_to_snake, camel_or_snake_to_title, get_admin, two_item_tuple_to_dict
from django_user_role.exceptions import RoleDoesNotExist

registered_roles = {}

logger = logging.getLogger()


class RolesManager(object):

    def __iter__(cls):
        return iter(registered_roles)

    @classmethod
    def retrieve_role(cls, role_name):
        if role_name in registered_roles:
            return registered_roles[role_name]

    @classmethod
    def get_roles_names(cls):
        return registered_roles.keys()

    @classmethod
    def get_roles(cls):
        return registered_roles.values()


def init_add_role_into_db(app_name, role_name, permisson_list):
    try:
        role_instance, _created = Role.objects.get_or_create(name=role_name,
                                                             app_scope=app_name)
        role_instance.permissions.add(*permisson_list)
    except Exception:
        logger.error('init roles has error!!!', exc_info=True)


class BasicMixin(object):
    """
    创建db中的role记录时,名字即为其class的名字
    创建role相关的permission时,会将其permission前加上app_name前缀
    """

    @classmethod
    def get_app_name(cls):
        return cls.get_module_name().split('.')[0]

    @classmethod
    def get_module_name(cls):
        return cls.__module__

    @classmethod
    def get_name(cls):
        if hasattr(cls, 'role_name'):
            return cls.role_name
        return camel_to_snake(cls.__name__)

    @classmethod
    def get_role(cls):
        return Role.objects.get(name=cls.get_name())

    @classmethod
    def permission_names_list(cls):
        permissions = getattr(cls, 'permissions', [])
        wrap_names = [cls._wrap_permission_name(name[0]) for name in permissions]
        return wrap_names

    @classmethod
    def permission_list(cls):
        return getattr(cls, 'permissions', [])

    @classmethod
    def get_role_permissions(cls):
        permission_list = cls.permission_list()
        return cls.get_or_create_permissions(permission_list)

    @classmethod
    def _wrap_permission_name(cls, permission_name):
        return "%s_%s" % (cls.get_app_name(), permission_name)

    @classmethod
    def get_or_create_permissions(cls, permission_list):
        ct = ContentType.objects.get(app_label=cls.get_app_name(), model='permission')
        # 0 is code 1 is describe
        permission_names = [name_value[0] for name_value in permission_list]
        name_dict = two_item_tuple_to_dict(permission_list)
        permissions = list(Permission.objects.filter(
            content_type=ct, codename__in=permission_names).all())

        missing_permissions = set(permission_names) - set((p.codename for p in permissions))
        if len(missing_permissions) > 0:
            for permission_name in missing_permissions:
                if name_dict.get(permission_name, None):
                    permission, created = get_or_create_permission(ct, permission_name,
                                                                   name=name_dict.get(permission_name, None))
                else:
                    permission, created = get_or_create_permission(ct, permission_name)

                permissions.append(permission)

        return permissions

    @classmethod
    @transaction.atomic
    def remove_role_from_user(cls, user):
        role = cls.get_role()
        user.role_set.remove(role)
        permissions = cls.get_role_permissions()
        for permission in permissions:
            try:
                PermissionRefCount.objects.get(user=user,
                                               permission=permission,
                                               role=role).delete()
            except PermissionRefCount.DoesNotExist:
                pass
            if not PermissionRefCount.objects.filter(user=user, permission=permission).exists():
                user.user_permissions.remove(permission)
        return role

    @classmethod
    def assign_role_to_user(cls, user):
        defaults = dict(user_create=get_admin())
        role_instance, _created = Role.objects.get_or_create(defaults=defaults,
                                                             name=cls.get_name(),
                                                             app_scope=cls.get_app_name())
        user.role_set.add(role_instance)
        permissions = cls.get_role_permissions()
        user.user_permissions.add(*permissions)
        for permission in permissions:
            PermissionRefCount.objects.get_or_create(user=user,
                                                     permission=permission,
                                                     role=role_instance)

        return role_instance


class RolesClassRegister(type):

    def __new__(cls, name, parents, dct):
        role_class = super(RolesClassRegister, cls).__new__(cls, name, parents, dct)

        if BasicMixin not in parents:
            registered_roles[role_class.get_name()] = role_class
            init_add_role_into_db(role_class.get_app_name(), role_class.get_name(), role_class.get_role_permissions())
        return role_class


@add_metaclass(RolesClassRegister)
class AbstractUserRoleGroup(BasicMixin):

    @classmethod
    def role_names_list(cls):
        roles = getattr(cls, 'roles', [])

        return [role.get_name() for role in roles]

    @classmethod
    def permission_list(cls):
        permissions = getattr(cls, 'permissions', [])
        for role in getattr(cls, 'roles', []):
            permissions.extend(role.permission_list())
        return permissions

    @classmethod
    def permission_names_list(cls):
        permissions = super(AbstractUserRoleGroup, cls).permission_names_list()
        roles = getattr(cls, 'roles', [])
        for role in roles:
            permissions.extend(role.permission_names_list())

        return permissions


@add_metaclass(RolesClassRegister)
class AbstractUserRole(BasicMixin):
    pass


def get_or_create_permission(ct, codename, name=camel_or_snake_to_title):
    return Permission.objects.get_or_create(content_type=ct, codename=codename,
                                            defaults={'name': name(codename) if callable(name) else name})


def retrieve_role(role_name):
    return RolesManager.retrieve_role(role_name)


def get_user_roles(user):
    if user:
        role_queryset = user.role_set.all()
        roles = (RolesManager.retrieve_role(role.name) for role in role_queryset if
                 role.name in RolesManager.get_roles_names())
        return sorted(roles, key=lambda r: r.get_name())
    else:
        return []


def _assign_or_remove_role(user, role, method_name):
    role_cls = role
    if not inspect.isclass(role):
        role_cls = retrieve_role(role)

    if not role_cls:
        raise RoleDoesNotExist

    getattr(role_cls, method_name)(user)

    return role_cls


def assign_role(user, role):
    return _assign_or_remove_role(user, role, "assign_role_to_user")


def remove_role(user, role):
    return _assign_or_remove_role(user, role, "remove_role_from_user")


def clear_roles(user):
    roles = get_user_roles(user)

    for role in roles:
        role.remove_role_from_user(user)

    return roles
