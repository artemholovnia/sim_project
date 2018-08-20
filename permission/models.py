from django.db import models
from django.apps import apps
from django.contrib.auth.models import User

# Create your models here.
class ModelPermission(models.Model):
    model_name = models.CharField(max_length=128, blank=False, null=True, default=None, verbose_name='model name')
    permission_name = models.CharField(max_length=128, blank=False, null=True, default=None, verbose_name='permission name')
    description = models.CharField(max_length=256, blank=False, null=True, default=None, verbose_name='description')
    tag = models.CharField(max_length=1, blank=False, null=True, default=None, verbose_name='tag')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='created at', editable=False)
    updated_at = models.DateTimeField(auto_now=True, blank=True, verbose_name='updated at', editable=False)

    def __str__(self):
        return '{description} (model_name: {model_name}, id: {id}, permission_name: {permission_name})'.format(description=self.description, model_name=self.model_name.upper(), id=self.id, permission_name=self.permission_name)

    class Meta:
        db_table = 'model_permissions'

class PermissionGroup(models.Model):
    model_permissions = models.ManyToManyField(ModelPermission, verbose_name='model permissions')
    name = models.CharField(max_length=16, unique=True, blank=False, default=None, verbose_name='name')
    permissions = models.CharField(max_length=512, blank=True, null=True, default=None, verbose_name='permissions', editable=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='created at', editable=False)
    updated_at = models.DateTimeField(auto_now=True, blank=True, verbose_name='updated at', editable=False)

    class Meta:
        db_table = 'permission_groups'

    def __str__(self):
        return self.name

