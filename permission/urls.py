from django.urls import re_path
from .views import *

urlpatterns = [
    re_path(r'^permission_groups/$', CreatePermissionGroupView.as_view(), name='create_permission_group'),
    re_path(r'^group_detail/group=(?P<id>[0-9]{1,100})/$', GroupDetailView.as_view(), name='group_detail'),

    re_path(r'^group_detail_functions/$', GroupDetailFunctions.as_view(), name='group_detail_functions'),
]