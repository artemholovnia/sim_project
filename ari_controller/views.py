from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.views.generic import TemplateView, FormView
import json
from peewee import DoesNotExist as DoesNotExistDatabase
from peewee import IntegrityError as IntegrityErrorDatabase
from peewee import OperationalError as OperationalErrorDatabase
from user_auth.views import MainInfo

# Create your views here.
class ChannelsController(MainInfo):
    template_name = 'ari_controller/channels_controller.html'

from .forms import CreateSipUserForm
class CreateSipUserView(MainInfo):
    template_name = 'ari_controller/create_sip_user.html'

    def post(self, *args, **kwargs):
        user_data = self.request.POST
        form_fields = [field for field in CreateSipUserForm().fields]
        form_data = {}
        #{'name':user_data.get('name'), 'username':user_data.get('username'), 'secret':user_data.get('secret')}
        for key in user_data.keys():
            if key in form_fields and len(user_data.get(key)) != 0:
                form_data.update({key:user_data.get(key)})
                # setattr(user_sip_form, key, user_data.get(key))
                print('Переменной {field} присвоено значение {value}'.format(field=key, value=user_data.get(key)), len(user_data.get(key)))
        print(form_data)
        user_form = CreateSipUserForm(form_data)
        if user_form.is_valid():
            user_form.save_user(form_data)
        else:
            print(user_form.errors)
        return redirect(reverse('start_page'))

    def get_context_data(self, **kwargs):
        context = super(CreateSipUserView, self).get_context_data(**kwargs)
        context['create_sip_user_form'] = CreateSipUserForm
        return context

from .forms import CreateBridgeForm, BridgeModel
class CreateBridgeView(MainInfo):
    template_name = 'ari_controller/create_bridge.html'

    def get_context_data(self, **kwargs):
        context = super(CreateBridgeView, self).get_context_data(**kwargs)
        context['create_bridge_form'] = CreateBridgeForm
        return context

    def post(self, *args, **kwargs):
        if self.request.is_ajax():
            if self.request.POST.get('function') == 'get_active_bridges':
                try:
                    bridges = BridgeModel.select()
                    bridges_list = []
                    for bridge in bridges:
                        bridges_list.append({'context':bridge.context, 'exten':bridge.exten, 'priority':bridge.priority, 'app':bridge.app, 'appdata':bridge.appdata})
                    return JsonResponse(data=json.dumps({'success':True, 'bridges_list':bridges_list}), safe=False)
                except OperationalErrorDatabase:
                    return JsonResponse(data={'success':False, 'code':"databaseConnectionError", 'message':'Wystapil blad polaczenia do bazy dannych'})
            if self.request.POST.get('function') == 'create_bridge':
                post_data = self.request.POST
                form_fields = [field for field in CreateBridgeForm().fields]
                form_data = {}
                for key in post_data:
                    if key in form_fields and len(post_data.get(key)) != 0:
                        form_data.update({key: post_data.get(key)})
                create_bridge_form = CreateBridgeForm(form_data)
                if create_bridge_form.is_valid():
                    try:
                        create_bridge_form.save_bridge(form_data)
                        return JsonResponse(data={'success':True, 'message':'Mostek z identyfikatorem {bridge_id} zostal dodany'.format(bridge_id=post_data.get('exten'))}, status=200)
                    except IntegrityErrorDatabase:
                        return JsonResponse(data={'success':False, 'message':'Mostek z identyfikatorem {bridge_id} juz istnieje'.format(bridge_id=post_data.get('exten'))})
                else:
                    return JsonResponse(data={'success':False})
            if self.request.POST.get('function') == 'delete_bridge':
                bridge_id=self.request.POST.get('bridge_id', None)
                try:
                    bridge = BridgeModel.get(exten=bridge_id)
                    bridge.delete_instance()
                    return JsonResponse({'success':True, 'message':'Mostek z idyntyfikatorem {bridge_id} zostal usuniety'.format(bridge_id=bridge_id)})
                except DoesNotExistDatabase:
                    return JsonResponse({'success':False, 'message':'Nie znalezniono mustku z identyfikatorem {bridge_id}'.format(bridge_id=bridge_id)})
        return redirect(reverse('create_bridge'))


