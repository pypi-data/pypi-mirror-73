from django.contrib import admin
from django.contrib import messages
from django_user_role.models import (
    Role,
    PermissionRefCount
)

from django_user_role.role import retrieve_role, get_user_roles


@admin.register(PermissionRefCount)
class PermissionRefCountAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'permission')
    search_fields = ('user__username', 'role__name', 'permission__name')


"""
class AdminUser(AbstractUserRole):

    @classmethod
    def auto_match_user(cls):
        user = User.objects.get(is_superuser=True, username='admin')
        cls.get_role().users.add(user)


class SuperUser(AbstractUserRole):

    @classmethod
    def auto_match_user(cls):
        user = User.objects.filter(is_superuser=True)
        cls.get_role().users.add(*user)
"""


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    filter_horizontal = ('permissions', 'user_groups', 'users')
    list_display = ('name', 'app_scope', 'user_count', 'permission_count')

    search_fields = ['permissions__codename', 'users__username']

    actions = ['auto_match_user']

    def permission_count(self, obj):
        return len(obj.permissions.all())

    def user_count(self, obj):
        return len(obj.users.all())

    def auto_match_user(self, request, queryset):
        try:

            for instance in queryset:
                role = retrieve_role(instance.name)
                if hasattr(role, 'auto_match_user'):
                    role.auto_match_user()
                    messages.success(request, '%s update success！' % instance.name)
                else:
                    messages.warning(request, '%s no auto match method' % instance.name)
        except:
            messages.error(request, 'action exec error!')

    auto_match_user.short_description = 'search&update user'

    def save_model(self, request, obj, form, change):
        if 'users' in form.changed_data:
            role = retrieve_role(obj.name)

            if role:
                current_users = form.cleaned_data['users']
                previous_users = obj.users.all()

                for removed in set(previous_users).difference(set(current_users)):
                    role.remove_role_from_user(removed)
                    roles = get_user_roles(removed)
                    for role in roles:
                        role.assign_role_to_user(removed)
                for user in set(current_users).difference(set(previous_users)):
                    role.assign_role_to_user(user)
        obj.save()
