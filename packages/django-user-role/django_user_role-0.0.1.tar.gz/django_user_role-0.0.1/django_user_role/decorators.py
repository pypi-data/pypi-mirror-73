from functools import wraps
from django_user_role.utils import user_is_authenticated
from django_user_role.checkers import has_role, has_permission


def has_role_decorator(role_names):
    def request_decorator(dispatch):
        @wraps(dispatch)
        def wrapper(*args, **kwargs):
            self = args[0]
            request = args[1]
            user = request.user
            if user_is_authenticated(user):
                for role in role_names:
                    if has_role(user, role):
                        return dispatch(*args, **kwargs)

            self.permission_denied(request, None)

        return wrapper

    return request_decorator


def has_permission_decorator(permission_name):
    def request_decorator(dispatch):
        @wraps(dispatch)
        def wrapper(*args, **kwargs):

            self = args[0]
            request = args[1]
            user = request.user
            if user_is_authenticated(user):
                if has_permission(user, permission_name):
                    return dispatch(*args, **kwargs)
            self.permission_denied(request, None)

        return wrapper

    return request_decorator
