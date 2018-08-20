from django.shortcuts import render, redirect, reverse
from permission.check_permission import Permission as UserCheckPermission
from permission.forms import CreatePermissionGroupForm
from django.views.generic import TemplateView, DetailView
from django.http import JsonResponse, HttpResponse
import json
from permission.models import PermissionGroup, ModelPermission
from user_auth.models import UserProfile
from user_auth.views import MainInfo
from django.db.models import Q
from django.forms import BaseForm
from django.contrib.auth.models import User

# Create your views here.

class PermissionGroupMain(MainInfo):
    template_name = 'permissions/permission_group.html'
    model_name = 'permissiongroup'

    def get_context_data(self, **kwargs):
        context = super(PermissionGroupMain, self).get_context_data(**kwargs)
        context['createPermissionGroup_permission'] = UserCheckPermission(self.request, 'permissiongroup', tag='C').__call__()
        context['updatePermissionGroup_permission'] = UserCheckPermission(self.request, 'permissiongroup', tag='U').__call__()
        context['deletePermissionGroup_permission'] = UserCheckPermission(self.request, 'permissiongroup', tag='D').__call__()
        context['viewPermissionGroup_permission'] = UserCheckPermission(self.request, 'permissiongroup', tag='V').__call__()
        context['createPermissionGroupForm'] = CreatePermissionGroupForm
        context['activeGroups'] = PermissionGroup.objects.all()
        return context

class CreatePermissionGroupView(PermissionGroupMain):
    template_name = 'permissions/permission_group.html'

    def post(self, *args, **kwargs):
        if self.request.is_ajax():
            form = CreatePermissionGroupForm({'name':self.request.POST.get('name'), 'model_permissions':json.loads(self.request.POST.get('permissions'))})
            if form.errors:
                errors_list = []
                for error in form.errors:
                    error_dict = {'field_name':error, 'message':form.errors.get(error)[0]}
                    errors_list.append(error_dict)
                return JsonResponse({'success':False, 'errors':errors_list})
            else:
                created_group = PermissionGroup.objects.create(name=form.cleaned_data.get('name'))
                created_group.model_permissions.set(form.cleaned_data.get('model_permissions'))
                print(created_group.name, created_group.id)
            return JsonResponse({'success':True})
        else:
            return redirect(reverse('create_permission_group'))

    def get(self, *args, **kwargs):
        user_permission = UserCheckPermission(self.request, self.model_name).__call__()
        if user_permission:
            return super(CreatePermissionGroupView, self).get(*args, **kwargs)
        else:
            return HttpResponse('permission denied')

    def get_context_data(self, **kwargs):
        context = super(CreatePermissionGroupView, self).get_context_data(**kwargs)
        return context

class GroupDetailView(DetailView, PermissionGroupMain):
    template_name = 'permissions/group_detail.html'
    slug_field = 'id'
    pk_url_kwarg = 'id'
    model = PermissionGroup
    context_object_name = 'group'

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super(GroupDetailView, self).get_context_data(**kwargs)
        context['users'] = UserProfile.objects.filter(permission_group=self.object)
        context['model_permissions'] = self.object.model_permissions.all()
        return context

    def get(self, *args, **kwargs):
        if UserCheckPermission(self.request, self.model_name, tag='U').__call__() or UserCheckPermission(self.request, self.model_name, tag='C').__call__() or UserCheckPermission(self.request, self.model_name, tag='D').__call__():
            return super(GroupDetailView, self).get(*args, **kwargs)
        else:
            return HttpResponse('permission denied')

class GroupDetailFunctions(TemplateView):
    template_name = 'permissions/group_detail.html'

    def post(self, *args, **kwargs):
        if self.request.is_ajax():
            request_dict = self.request.POST
            if request_dict.get('function') == 'add_permission_to_group':
                permissions_to_show = ModelPermission.objects.exclude(Q(id__in=[permission.id for permission in PermissionGroup.objects.get(id=int(request_dict.get('group_id'))).model_permissions.all()]))
                form = CreatePermissionGroupForm()
                form.fields.get('model_permissions').queryset = permissions_to_show
                form.fields.pop('name')
                return JsonResponse({'success':True, 'form':form.as_ul()})

            if request_dict.get('function') == 'update_group_permissions':
                print(request_dict.get('permissions').split(','))
                model_permissions = PermissionGroup.objects.get(id=int(request_dict.get('group_id'))).model_permissions
                for model_permission_id in request_dict.get('permissions').split(','):
                    model_permissions.add(ModelPermission.objects.get(id=int(model_permission_id)))
                return JsonResponse({'success':True})

            if request_dict.get('function') == 'user_list':
                user_list = []
                users = None
                if request_dict.get('filter') is not None:
                    users = UserProfile.objects.filter(Q(username__icontains=request_dict.get('searched_username')))
                    if len(users) == 0:
                        return JsonResponse({'success':False, 'message':'Nie znalezniono profilu uzytkownika z podana nazwa'})
                if users is not None:
                    for user in users:
                        if PermissionGroup.objects.get(id=request_dict.get('group_id')) not in user.permission_group.all():
                            user_list.append({'username':user.user.username, 'user_id':user.user.id, 'profile_id':user.id})
                        else:
                            pass
                return JsonResponse({'success':True, 'users':user_list})

            if request_dict.get('function') == 'add_user_to_group':
                group = PermissionGroup.objects.get(id=request_dict.get('group_id'))
                user_profile = UserProfile.objects.get(user=User.objects.get(id=request_dict.get('user_id')))
                user_profile.permission_group.add(group)
                return JsonResponse({'success':True, 'username':user_profile.username, 'group':group.__str__()})

            if request_dict.get('function') == 'delete_permission_from_group':
                PermissionGroup.objects.get(id=request_dict.get('group_id')).model_permissions.remove(ModelPermission.objects.get(id=request_dict.get('permission_id')))
                return JsonResponse({'success':True})

            if request_dict.get('function') == 'delete_user_profile_from_group':
                UserProfile.objects.get(id=request_dict.get('user_profile_id')).permission_group.remove(PermissionGroup.objects.get(id=request_dict.get('group_id')))
                return JsonResponse({'success':True})

        else:
            return HttpResponse('bad request')
