from django.urls.conf import re_path
from .views import *

urlpatterns = [
    re_path(r'^channels/$', ChannelsController.as_view(), name='channels_controller')
]