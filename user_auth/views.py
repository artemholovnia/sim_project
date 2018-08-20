from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse
from django.views.generic import FormView, TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView
from .models import UserProfileImage, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from permission.models import ModelPermission
from permission.check_permission import Permission as UserPermissionCheck
# Create your views here.

class MainInfo(TemplateView):
    template_name='main_template.html'

    def get_context_data(self, **kwargs):
        context = super(MainInfo, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        context['createUserRegistration_permission'] = UserPermissionCheck(self.request, 'user', tag='C').__call__()
        context['PermissionGroup_permission'] = UserPermissionCheck(self.request, 'permissiongroup').__call__()
        context['xml_permission'] = UserPermissionCheck(self.request, 'xml').__call__()
        return context

#test
class Users(ListView, MainInfo):
    template_name = 'user_auth/users.html'
    model = User
    context_object_name = 'users'

    def get_context_data(self, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = super(Users, self).get_context_data(*args, **kwargs)
        context['user_images'] = UserProfileImage.objects.all()
        return context

    def post(self, *args, **kwargs):
        if self.request.is_ajax():
            request_dict = self.request.POST
            return JsonResponse({'success':True, 'image': UserProfileImage.objects.get(user=User.objects.get(id=request_dict.get('user_id'))).image.url})

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return super(Users, self).get(*args, **kwargs)
        else:
            return redirect(reverse('start_page'))

#test
class UserDetail(DetailView):
    template_name = 'user_auth/user_detail.html'
    model = User
    context_object_name = 'user'
    slug_url_kwarg = 'id'
    slug_field = 'id'

    def get_object(self, **kwargs):
        object = self.model._default_manager.get(id=self.kwargs.get(self.slug_url_kwarg))
        return object

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super(UserDetail, self).get_context_data(**kwargs)
        context['profileImage'] = UserProfileImage.objects.get(user=self.object)
        return context

#user registration
from .forms import UserRegistrationForm, UserProfileImageForm
from permission.check_permission import  Permission as UserPermissionCheck
class UserRegistrationView(TemplateView):
    template_name = 'user_auth/user_registration.html'
    model_name = 'user'
    tag = 'C'

    def get_app_permission(self):
        allow_permissions = [permission.permission_name for permission in ModelPermission.objects.filter(model_name='user')]
        return allow_permissions

    def get_context_data(self, **kwargs):
        context = super(UserRegistrationView, self).get_context_data(**kwargs)
        context['userRegistrationForm'] = UserRegistrationForm
        return context

    def post(self, *args, **kwargs):
        if self.request.is_ajax():
            request_dict = self.request.POST
            print(request_dict)
            form = UserRegistrationForm({'username':request_dict.get('username'), 'password':request_dict.get('password'), 'second_password':request_dict.get('second_password')})
            if form.is_valid():
                try:
                    existed_user = User.objects.get(username=form.cleaned_data.get('username'))
                    return JsonResponse({'success':False, 'errors':[{'field_name':'username', 'message':'Uzytkownik z nazwa {username} juz istnieje w systemie'.format(username=existed_user.username)}]})
                except User.DoesNotExist:
                    new_user = User.objects.create_user(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
                    #login(self.request, new_user)
                    return JsonResponse({'success':True})
            else:
                errors_list = []
                for error in form.errors:
                    one_error_dict = {}
                    one_error_dict.update({'field_name':str(error), 'message':form.errors.get(str(error))})
                    errors_list.append(one_error_dict)
                return JsonResponse({'success':False, 'errors':errors_list})
        else:
            return redirect(reverse('user_registration'))

    def get(self, *args, **kwargs):
        user_permission = UserPermissionCheck(self.request, self.model_name, self.tag).__call__() # 'user_C'
        if user_permission:
            return super(UserRegistrationView, self).get(*args, **kwargs)
        else:
            return HttpResponse('permission denied')

#login
from .forms import UserLoginForm
class Login(TemplateView):
    template_name = 'user_auth/user_login.html'

    def get_context_data(self, **kwargs):
        context = super(Login, self).get_context_data(**kwargs)
        context['userLoginForm'] = UserLoginForm
        return context

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse('users'))
        else:
            return super(Login, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        if  self.request.is_ajax():
            request_dict = self.request.POST
            form = UserLoginForm({'username':request_dict.get('username'), 'password':request_dict.get('password')})
            if form.is_valid():
                try:
                    existed_user = User.objects.get(username=request_dict.get('username'))
                    if existed_user.check_password(request_dict.get('password')):
                        login(self.request, existed_user)
                        return JsonResponse({'success':True, 'redirect_url':reverse_lazy('users')})
                    else:
                        return JsonResponse({'success': False, 'errors': [{'field_name': 'password', 'message': 'Wpisane niepoprawne danne, prosze sprobowac jeszcze raz'}]})
                except User.DoesNotExist:
                    return JsonResponse({'success': False, 'errors': [{'field_name': 'password', 'message': 'Wpisane niepoprawne danne, prosze sprobowac jeszcze raz'}]})
            else:
                return JsonResponse({'success':False, 'errors':[{'field_name':'password', 'message':'Wpisane niepoprawne danne, prosze sprobowac jeszcze raz'}]})
        else:
            return super(Login, self).get(*args, **kwargs)

def user_logout(request):
    logout(request)
    return redirect(reverse('start_page'))

#start page
class StartPage(TemplateView):
    template_name = 'client/start_page.html'

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse('users'))
        else:
            return super(StartPage, self).get(*args, **kwargs)



