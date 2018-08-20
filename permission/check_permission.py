from permission.models import PermissionGroup, ModelPermission
from user_auth.models import UserProfile
from django.contrib.auth.models import User
from django.core.exceptions import FieldError
from django.http import HttpResponse

class Permission:
    def __init__(self, request, model_name, tag=None):
        self.request = request
        self.model_name = model_name
        self.tag = tag

    def __call__(self):
        if self.model_name is not None:
            have_access = self.have_access()
            return have_access
        else:
            pass

    def get_user_permissions(self): #права доступа авторизированного пользователя
        user_permissions_list = []
        if self.request.user.is_authenticated:
            try:
                user_profile = UserProfile.objects.get(user=self.request.user)
                [[user_permissions_list.append(permission.permission_name) for permission in group.model_permissions.all()] for group in user_profile.permission_group.all()]
                #print('user permissions ', user_permissions_list)
                return user_permissions_list
            except UserProfile.DoesNotExist:
                raise ValueError('user profile does not exist')
        else:
            return HttpResponse('user is not authenticated')

    def have_access(self): #
        have_permission = False
        user_permissions_list = self.get_user_permissions() #user_C, user_U
        if self.tag is not None:
            for permission in user_permissions_list:
                if permission == '_'.join([self.model_name, self.tag]): #if user_C == user_C
                    #print('have')
                    have_permission = True
        else:
            if user_permissions_list is not None and self.model_name is not None:
                model_permissions = self.get_model_permissions() #user_C, user_U, user_D
                for permission in user_permissions_list:
                    if permission in model_permissions:
                        have_permission = True
            else:
                raise ValueError('please run get_user_permission method before runing this')
        return have_permission

    def get_model_permissions(self):
        if self.model_name is not None:
            model_permissions = [permission.permission_name for permission in ModelPermission.objects.filter(model_name=self.model_name)]
            return model_permissions
        else:
            raise FieldError('NoneType object has no permissions')