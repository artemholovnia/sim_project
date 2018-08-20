from django.urls import re_path
from user_auth.views import *

urlpatterns = [
    #path('^login/$', UserAuth.as_view(), name='login'),
    re_path(r'^$', StartPage.as_view(), name='start_page'),
    re_path(r'^users/', Users.as_view(), name='users'),
    re_path(r'^user_detail=(?P<id>[0-9]+)/$', UserDetail.as_view(), name='user_detail'),

    re_path(r'^user_registration/$', UserRegistrationView.as_view(), name='user_registration'),
    re_path(r'^login/$', Login.as_view(), name='login'),
    re_path(r'^logout/$', user_logout, name='logout'),

]