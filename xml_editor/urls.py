from django.urls import re_path
from .views import *

urlpatterns = [
    re_path(r'^edit/$', CreateXML.as_view(), name='create_xml'),
    re_path(r'^delete_file/file_id=(?P<file_id>[0-9]{1,100})/$', delete_xml_model, name='delete_file'),
    re_path(r'^show/path=(?P<path>.+)/$', show_document, name='show'),
]