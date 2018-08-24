from django.forms import Form, CharField, IntegerField, Select, TextInput, NumberInput, PasswordInput
from django.utils.deconstruct import deconstructible
from django.core.validators import BaseValidator, RegexValidator
from django.core.exceptions import ValidationError

#@deconstructible
#class UniqueSipValidator(BaseValidator):
#    message='Unique error message'
#    def __init__(self, name, message=None):
#        self.name=name
#        if message:
#            self.message=message

#    def

from peewee import DoesNotExist as DoesNotExistSQL
class CreateSipUserForm(Form):
    name=CharField(max_length=80, min_length=1, required=True, label='Nazwa uzytkownika', widget=TextInput(attrs={'class':'form-control', 'autocomplete':'no'}))
    username=CharField(max_length=80, required=False, label='Username', widget=TextInput(attrs={'class':'form-control', 'autocomplete':'no'}))
    secret=CharField(max_length=80, min_length=4, required=True, label='Haslo', widget=PasswordInput(attrs={'class':'form-control', 'autocomplete':'no'}))
    nat=CharField(label='nat', required=False, widget=Select(attrs={'class':'form-control'}, choices=( (None, '---'), ('yes', 'yes'), ('no', 'no') )))
    type=CharField(label='type', required=False, widget=Select(attrs={'class':'form-control'}, choices=( (None, '---'), ('friend', 'friend'), ('user', 'user'), ('peer', 'peer') )))
    qualify=CharField(label='qualify', required=False, widget=Select(attrs={'class':'form-control'}, choices=( (None, '---'), ('yes', 'yes'), ('no', 'no') ) ))
    allowoverlap=CharField(label='allowoverlap', required=False, widget=Select(attrs={'class':'form-control'}, choices=( (None, '---'), ('yes', 'yes'), ('no', 'no') ) ))
    allowsubscribe=CharField(label='allowsunscrive', required=False, widget=Select(attrs={'class':'form-control'}, choices=( (None, '---'), ('yes', 'yes'), ('no', 'no') ) ))
    allowtransfer=CharField(label='allowtransfer', required=False, widget=Select(attrs={'class':'form-control'}, choices=( (None, '---'), ('yes', 'yes'), ('no', 'no') ) ))
    ignoresdpversion=CharField(label='ignorespdversion', required=False, widget=Select(attrs={'class':'form-control'}, choices=( (None, '---'), ('yes', 'yes'), ('no', 'no') ) ))
    videosupport=CharField(label='videosupport', required=False, widget=Select(attrs={'class':'form-control'}, choices=( (None, '---'), ('yes', 'yes'), ('no', 'no') ) ))
    rfc2833compensate=CharField(label='rfc2833compensate', required=False, widget=Select(attrs={'class':'form-control'}, choices=( (None, '---'), ('yes', 'yes'), ('no', 'no') ) ))

    def __init__(self, *args, **kwargs):
        super(CreateSipUserForm, self).__init__(*args, **kwargs)
        self.fields.get('name').validators.append(RegexValidator(r'^[\w]+$', 'Pole moze zawierac tylko cyfry od 0 do 9, litery a-Z i _'))
        self.fields.get('username').validators.append(RegexValidator(r'^[\w.]+$', 'Pole moze zawierac tylko symboli a-Z _ .'))

    def clean(self):
        try:
            existed_user = SipUserModel.get(name=self.cleaned_data.get('name'))
            self.add_error('name', 'Uzytkownik z nazwa {name} juz zarejestrowany s systemie'.format(name=self.cleaned_data.get('name')))
            raise ValidationError('Not a unique name', code='unique name error')
        except DoesNotExistSQL:
            pass
        return self.cleaned_data

    def save_user(self, form_data):
        user = SipUserModel()
        for key in form_data.keys():
            if hasattr(user, key):
                setattr(user, key, form_data.get(key))
        user.save()
        print('User with name {name} created'.format(name=self.cleaned_data.get('name')))
        return user

class CreateBridgeForm(Form):
    context=CharField(max_length=20, required=False, label='Kontekst', widget=TextInput(attrs={'value':'polaczenia', 'readonly':'true', 'class':'form-control'}))
    exten=CharField(max_length=20, required=True, label='ID mostku', widget=TextInput(attrs={'class':'form-control'}))
    priority=IntegerField(required=False, label='Prioritet', widget=NumberInput(attrs={'value':1, 'readonly':'true', 'class':'form-control'}))
    app=CharField(max_length=20, required=True, label='Aplikacja', widget=TextInput(attrs={'value':'ConfBridge', 'readonly':'true', 'class':'form-control'}))
    appdata=CharField(max_length=20, required=False, label='Nazwa mostku (czytelna)', widget=TextInput(attrs={'class':'form-control'}))

    def __init__(self, *args, **kwargs):
        super(CreateBridgeForm, self).__init__(*args, **kwargs)

    def save_bridge(self, form_data):
        bridge = BridgeModel()
        for key in form_data:
            if hasattr(bridge, key):
                setattr(bridge, key, form_data.get(key))
        bridge.save()
        print('Bridge with id {bridge_id} created'.format(bridge_id=form_data.get('appdata')))
        return bridge


from playhouse.pool import PooledMySQLDatabase
from sim.settings import RASPBERRY, ASTERISK_DATABASE
if RASPBERRY:
    prod_op = ASTERISK_DATABASE.get('PROD_OP')
    DB = PooledMySQLDatabase(prod_op.get('name'), user=prod_op.get('user'), password=prod_op.get('password'), port=prod_op.get('port'), host=prod_op.get('host'))
else:
    dev_op = ASTERISK_DATABASE.get('DEV_OP')
    DB = PooledMySQLDatabase(dev_op.get('name'), user=dev_op.get('user'), password=dev_op.get('password'), port=dev_op.get('port'), host=dev_op.get('host'))

from peewee import Model, CharField, IntegerField
from django.utils.timezone import datetime
class SipUserModel(Model):
    name=CharField(max_length=80, unique=True, null=False)
    username=CharField(max_length=80, null=False)
    secret=CharField(max_length=80, null=True, default=None)
    allow=CharField(max_length=100, null=True, default='alaw')
    disallow=CharField(max_length=100, null=True, default='all')
    host=CharField(max_length=31, null=True, default='dynamic')
    context=CharField(max_length=80, null=True, default='polaczenia')

    nat=CharField(max_length=5, null=False, default='no')
    type=CharField(max_length=10, null=False, default='friend')
    qualify=CharField(max_length=3, null=True, default=None)
    allowoverlap=CharField(max_length=3, null=False, default='yes')
    allowsubscribe=CharField(max_length=3, null=False, default='yes')
    allowtransfer=CharField(max_length=3, null=False, default='yes')
    ignoresdpversion=CharField(max_length=3, null=False, default='no')
    videosupport=CharField(max_length=5, null=False, default='no')
    rfc2833compensate=CharField(max_length=3, null=False, default='yes')

    fullcontact=CharField(max_length=80, default='')
    ipaddr=CharField(max_length=15, default='')
    defaultuser=CharField(max_length=80, default='')
    regserver=CharField(max_length=100, default='')
    useragent=CharField(max_length=50, default='')

    class Meta:
        database = DB
        table_name = 'sip'

class BridgeModel(Model):
    context=CharField(max_length=20, null=False, default='polaczenia')
    exten=CharField(max_length=20, null=False)
    priority=IntegerField(null=False)
    app=CharField(max_length=20, null=False)
    appdata=CharField(max_length=128, null=False)

    class Meta:
        database = DB
        table_name = 'extensions'









