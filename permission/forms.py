from django.forms import ModelForm, Form, CheckboxSelectMultiple, TextInput
from permission.models import PermissionGroup
from django.core import validators
from django.core.exceptions import ValidationError

class UniqueGroupValidator:
    def __init__(self, name, message=None, code=None):
        self.message = message
        self.code = code
        self.name = name

    def __call__(self):
        if self.message is None:
            self.message = u'Grupa z taka nazwa juz istnieje'
        try:
            PermissionGroup.objects.get(name=self.name)
            raise ValidationError(self.message)
        except PermissionGroup.DoesNotExist:
            pass

class CreatePermissionGroupForm(ModelForm):
    class Meta:
        model = PermissionGroup
        fields = ['model_permissions', 'name']
        widgets = {
            'name': TextInput(attrs={'class':'form-control'}),
            'model_permissions': CheckboxSelectMultiple(attrs={'class':'permission_models'}),
        }

    def __init__(self, *args, **kwargs):
        super(CreatePermissionGroupForm, self).__init__(*args, **kwargs)
        max_length_template = u'Maksymalna dlugosc nie powinna byc dluzsza za {limit_value}'
        min_length_template = u'Minimalna dlugosc nie powinna byc mniejsza za {limit_value}'
        self.fields.get('name').min_length = 4
        self.fields.get('name').validators.append(validators.MinLengthValidator(self.fields.get('name').min_length, message=min_length_template.format(limit_value=self.fields.get('name').min_length)))
        self.fields.get('name').error_messages = {'required':'To pole jest wymagane', 'max_length':max_length_template.format(limit_value=self.fields.get('name').max_length), 'unique':u'Grupa z taka nazwa juz istnieje'}
        self.fields.get('model_permissions').error_messages = {'required':'To pole jest wymagane'}

class SearchUsername(Form):
    from user_auth.forms import UserRegistrationForm
    username = UserRegistrationForm().fields.get('username')
