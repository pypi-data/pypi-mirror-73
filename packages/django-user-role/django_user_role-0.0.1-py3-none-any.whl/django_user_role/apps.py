from django.apps import AppConfig
from django_user_role.loader import load_roles_and_permissions


class AppBaseConfig(AppConfig):
    name = 'django_user_role'

    def ready(self):
        load_roles_and_permissions()
