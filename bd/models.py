# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthAssignment(models.Model):
    item_name = models.CharField(primary_key=True, max_length=64)
    user_id = models.CharField(max_length=64)
    created_at = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_assignment'
        unique_together = (('item_name', 'user_id'),)


class AuthItem(models.Model):
    name = models.CharField(primary_key=True, max_length=64)
    type = models.SmallIntegerField()
    description = models.TextField(blank=True, null=True)
    rule_name = models.CharField(max_length=64, blank=True, null=True)
    data = models.TextField(blank=True, null=True)
    created_at = models.IntegerField(blank=True, null=True)
    updated_at = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_item'


class AuthItemChild(models.Model):
    parent = models.CharField(primary_key=True, max_length=64)
    child = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'auth_item_child'
        unique_together = (('parent', 'child'),)


class AuthRule(models.Model):
    name = models.CharField(primary_key=True, max_length=64)
    data = models.TextField(blank=True, null=True)
    created_at = models.IntegerField(blank=True, null=True)
    updated_at = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_rule'


class Migration(models.Model):
    version = models.CharField(primary_key=True, max_length=180)
    apply_time = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'migration'


class Profile(models.Model):
    user_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    public_email = models.CharField(max_length=255, blank=True, null=True)
    gravatar_email = models.CharField(max_length=255, blank=True, null=True)
    gravatar_id = models.CharField(max_length=32, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    timezone = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'profile'


class RoipClientConfig(models.Model):
    roip_client_config_id = models.AutoField(primary_key=True)
    roip_client_id = models.PositiveIntegerField()
    roip_client_config_type = models.PositiveIntegerField()
    roip_client_config_value = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'roip_client_config'


class RoipClientConfigTypes(models.Model):
    roip_client_config_type_id = models.AutoField(primary_key=True)
    roip_client_config_type_name = models.CharField(unique=True, max_length=45)
    roip_client_config_type_desc = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'roip_client_config_types'


class RoipClientTypes(models.Model):
    roip_client_type_id = models.AutoField(primary_key=True)
    roip_client_type_name = models.CharField(unique=True, max_length=45, blank=True, null=True)
    roip_client_type_desc = models.TextField(blank=True, null=True)
    roip_client_type_visible = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'roip_client_types'


class RoipDetectedClients(models.Model):
    roip_detected_clients_id = models.AutoField(primary_key=True)
    roip_client_mac = models.CharField(max_length=18)
    roip_client_serial = models.CharField(max_length=18)
    roip_client_type = models.IntegerField()
    roip_client_ip = models.CharField(max_length=18)
    roip_client_config_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'roip_detected_clients'


class RoipEnabledClients(models.Model):
    roip_enabled_client_id = models.AutoField(primary_key=True)
    roip_client_systemid = models.CharField(db_column='roip_client_systemID', unique=True, max_length=45)  # Field name made lowercase.
    roip_client_type = models.IntegerField()
    roip_client_mac = models.CharField(max_length=18)
    roip_client_serial = models.CharField(max_length=18)
    roip_client_connstring = models.CharField(db_column='roip_client_connString', max_length=255, blank=True, null=True)  # Field name made lowercase.
    roip_client_hasconfig = models.TextField(db_column='roip_client_hasConfig', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'roip_enabled_clients'


class Token(models.Model):
    user_id = models.IntegerField()
    code = models.CharField(max_length=32)
    created_at = models.IntegerField()
    type = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'token'
        unique_together = (('user_id', 'code', 'type'),)


