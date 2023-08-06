from importlib import import_module

from django.conf import settings
from django_user_role.utils import get_app_name


def load_roles_and_permissions():
    for app_name in settings.INSTALLED_APPS:
        if app_name is not 'app_base':
            app_name = get_app_name(app_name)
            try:
                import_module('.roles', app_name)
            except ImportError:
                pass
