from django.db import models
from django.contrib.auth.models import User as U
from django.utils.timezone import datetime
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.timezone import datetime
from permission.models import PermissionGroup

class UserProfile(models.Model):
    user = models.OneToOneField(U, on_delete=models.CASCADE, verbose_name='user id')
    username = models.CharField(unique=True, max_length=255, blank=True, null=True, default=None)
    email = models.CharField(unique=True, max_length=255, blank=True, null=True, default=None)
    password_hash = models.CharField(max_length=512)
    auth_key = models.CharField(max_length=32, blank=True, null=True, default=None)
    confirmed_at = models.DateTimeField(blank=True, null=True, default=None)
    unconfirmed_email = models.CharField(max_length=255, blank=True, null=True, default=None, verbose_name='unconfirmed email')
    blocked_at = models.DateTimeField(blank=True, null=True, default=None)
    registration_ip = models.CharField(max_length=45, blank=True, null=True, default=None, verbose_name='ip')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=False, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=False, verbose_name='updated at')
    flags = models.IntegerField(blank=True, null=True, default=None, verbose_name='flags')
    last_login_at = models.DateTimeField(blank=True, null=True, default=None)

    #permissions
    permission_group = models.ManyToManyField(PermissionGroup, blank=True, null=True, default=None, verbose_name='permission group')

    class Meta:
        db_table = 'user_profile'

    def __str__(self):
        return self.username

@receiver(post_save, sender=U)
def after_save_user(sender, instance, **kwargs):
    try:
        user_profile = UserProfile.objects.get(user=instance)
        user_profile.username = instance.username
        user_profile.password_hash = instance.password
        user_profile.save()
        print(user_profile.username,' user is updated')
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=instance, username=instance.username, password_hash=instance.password)
        print(user_profile.username,' user is created')

class UserProfileImage(models.Model):
    user = models.OneToOneField(U, on_delete=models.CASCADE, verbose_name='user id')
    image = models.ImageField(upload_to='user_images/', blank=True, null=True, default=None, verbose_name='image')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')

    def __str__(self):
        return 'username: %s, username_id: %i, image_path="%s" ' % (self.user.username, self.user.id, self.image.path)

    class Meta:
        db_table = 'user_profile_image'




