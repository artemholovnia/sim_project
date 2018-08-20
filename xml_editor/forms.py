from django.forms import Form, CharField
from django.core.validators import RegexValidator, MaxLengthValidator, MinLengthValidator
from .models import XML

FILES = (
    (0, '--------------'),
    ('RoIP_Box', 'RoIP_Box.xml'),
    ('RoIP_Console', 'RoIP_Console.xml'),
)

class CreateXMLForm(Form):
    file_name = CharField(label='Nazwa pliku', required=True)

    def __init__(self, *args, **kwargs):
        super(CreateXMLForm, self).__init__(*args, **kwargs)
        file_name_validators = [RegexValidator(regex=r'^[-/\w]+$', message='Niedopuszczalne symboli'),
                                MaxLengthValidator(limit_value=XML._meta.get_field('file_name').max_length, message='Dlugosc maksymalna {limit_value} symboli'.format(limit_value=XML._meta.get_field('file_name').max_length)),
                                MinLengthValidator(limit_value=2, message='Minimalna dlugosc {limit_value}'.format(limit_value=2))]
        [self.fields.get('file_name').validators.append(validator) for validator in file_name_validators]
        self.fields.get('file_name').error_messages.update({'required':'Pole jest wymagane'})


