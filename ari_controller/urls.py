from django.urls.conf import re_path
from .views import *

urlpatterns = [
    re_path(r'^channels/$', ChannelsController.as_view(), name='channels_controller'),
    re_path(r'^create_sip_user/$', CreateSipUserView.as_view(), name='create_sip_user'),
    re_path(r'^create_bridge/$', CreateBridgeView.as_view(), name='create_bridge'),
]