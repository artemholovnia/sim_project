class CreatePermissions():
    def __init__(self, app_names):
        self.app_names = app_names

    def create_permission(self, model_name):
        from permission.models import ModelPermission
        permission_tags = {'create':'C', 'update':'U', 'delete':'D', 'view':'V'}
        for key in permission_tags.keys():
            permission_name = '_'.join([model_name, permission_tags.get(key)])
            try:
                ModelPermission.objects.get(model_name=model_name, permission_name=permission_name)
                #print('{permission_name} is EXIST'.format(permission_name=permission_name))
            except ModelPermission.DoesNotExist:
                permission_description = '{tag_description} model \" {model_name} \"'.format(tag_description=key, model_name=model_name)
                create_permission = ModelPermission.objects.create(model_name=model_name, permission_name=permission_name, tag=permission_tags.get(key), description=permission_description)
                #print('{permission_name} is CREATED'.format(permission_name=permission_name))

    def apps(self):
        from django.apps import apps

        for app in self.app_names:
            models = apps.all_models.get(app)
            for model in models:
                self.create_permission(model)


