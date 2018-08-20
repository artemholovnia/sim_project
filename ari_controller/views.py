from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

class ChannelsController(TemplateView):
    template_name = 'ari_controller/channels_controller.html'

