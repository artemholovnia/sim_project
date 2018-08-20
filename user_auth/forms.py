from django.forms import Form, ModelForm, CharField, PasswordInput, TextInput
from .models import UserProfileImage, UserProfile
from django.core.validators import MaxLengthValidator, MinLengthValidator, RegexValidator
from django.contrib.auth.models import User
from .validators import UserUniqueValidator

class UserRegistrationForm(Form):
    username = CharField(min_length=4, max_length=32, widget=TextInput(attrs={'class':'form-control'}), error_messages={'required':u'Pole jest wymagane'})
    password = CharField(max_length=32, min_length=8, widget=PasswordInput(attrs={'class':'form-control'}), error_messages={'required':u'Pole jest wymagane'})
    second_password = CharField(max_length=32, min_length=8, widget=PasswordInput(attrs={'class':'form-control'}), error_messages={'required':u'Pole jest wymagane'})

    def __init__(self, *args, **kwargs):
        max_length_template = u'Maksymalna dlugosc nie powinna byc dluzsza za {limit_value}'
        min_length_template = u'Minimalna dlugosc nie powinna byc mniejsza za {limit_value}'
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        for field in ['username', 'password', 'second_password']:
            self.fields.get(field).validators = [MinLengthValidator(self.fields.get(field).min_length, message=min_length_template.format(limit_value=self.fields.get(field).min_length)),
                                                 MaxLengthValidator(self.fields.get(field).max_length, message=max_length_template.format(limit_value=self.fields.get(field).max_length))]
        self.fields.get('username').validators.append(RegexValidator(regex=r'^[\w._-]+$', message=u'Pole moze zawirac cyfry, litery ta ./_/-'))

class UserLoginForm(Form):
    parent = UserRegistrationForm()
    username = parent.fields.get('username')
    password = parent.fields.get('password')

class UserProfileImageForm(ModelForm):
    class Meta:
        model = UserProfileImage
        fields = ['image']
        labels = {'image':'Zdjencie uzytkownika'}