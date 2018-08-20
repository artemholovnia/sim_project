from django.db import models
from channels.layers import get_channel_layer

# Create your models here.

class Room(models.Model):
    title=models.CharField(max_length=16, blank=False, null=True, default=None, verbose_name='Room')



