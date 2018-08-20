from django.db import models
from django.contrib.auth.models import User
from user_auth.models import UserProfile
from django.dispatch import receiver
from django.db.models.signals import post_delete
import os

# Create your models here.
class XML(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False, verbose_name='user id')
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=True, default=None, null=True, verbose_name='user profile id')
    file_name = models.CharField(max_length=32, blank=False, unique=True, null=True, default=None, verbose_name='file name')
    type = models.CharField(max_length=4, blank=True, null=True, default=None, verbose_name='file format')
    file = models.FileField(upload_to='config_xmls/', blank=False, null=False, verbose_name='file')
    instant_editing = models.CharField(max_length=64, unique=True, blank=True, null=True, default=None, verbose_name='instant editing file')

    def __str__(self):
        return self.file_name

@receiver(post_delete, sender=XML)
def delete_file_after_delete_releted_model(sender, instance, **kwargs):
    if os.path.exists(instance.file.path):
        os.remove(instance.file.path)
    else:
       pass