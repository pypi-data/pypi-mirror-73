import re
import inspect
from pydoc import locate
import collections
from django.contrib.auth import get_user_model


def get_app_name(app_name):
    type_ = locate(app_name)
    if inspect.isclass(type_):
        return type_.name
    return app_name


def two_item_tuple_to_dict(item_list):
    return {item[0]: item[1] for item in item_list}


def get_admin():
    return get_user_model().objects.get(username='admin')


def camel_to_snake(s):
    _underscorer1 = re.compile(r'(.)([A-Z][a-z]+)')
    _underscorer2 = re.compile('([a-z0-9])([A-Z])')

    subbed = _underscorer1.sub(r'\1_\2', s)
    return _underscorer2.sub(r'\1_\2', subbed).lower()


def snake_to_title(s):
    return ' '.join(x.capitalize() for x in s.split('_'))


def camel_or_snake_to_title(s):
    return snake_to_title(camel_to_snake(s))


def user_is_authenticated(user):
    if isinstance(user.is_authenticated, collections.Callable):
        authenticated = user.is_authenticated()
    else:
        authenticated = user.is_authenticated

    return authenticated
