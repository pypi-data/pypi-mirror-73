from django.db import models
from django.contrib.auth.models import Permission, Group
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class PermissionRefCount(models.Model):
    """
    记录permission的引用计数,相同的permission可能属于多个role
    当删除role时,需要根据计数判断是否要删除permission

    todo 如果删除高级的role时,是否需要删除比它低级的role上的permission
    """
    # count 暂时无用
    count = models.IntegerField(default=1)

    user = models.ForeignKey('app_base.User', on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    role = models.ForeignKey('app_base.Role', on_delete=models.CASCADE)

    def __str(self):
        return "%s-%s-%s-%s-%s" % (self.user.username,
                                   self.role.name,
                                   self.permission.content_type.app_label,
                                   self.permission.content_type.model,
                                   self.permission.codename)


class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=500, null=True, blank=True)

    permissions = models.ManyToManyField(Permission,
                                         related_name='roles',
                                         related_query_name='roles', blank=True)
    app_scope = models.CharField(max_length=100, null=True, blank=True)

    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_('users'),
        null=True,
        blank=True,
        related_name='roles',
        related_query_name='roles'
    )

    user_groups = models.ManyToManyField(
        Group,
        verbose_name=_('user_groups'),
        null=True,
        blank=True,
        related_name='roles',
        related_query_name='roles'
    )

    def __str__(self):
        return self.name
