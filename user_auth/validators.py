from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
class UserUniqueValidator():
    def __init__(self, username, message=None, code=None):
        self.username = username
        self.message = message
        self.code = code

    def __call__(self):
        if self.message is None:
            self.message = u'Uzytkownik z taka nazwa juz jest zarejestrowany w systemie, prosze wprowadzic inna nazwe'
        try:
            user = User.objects.get(username=self.username)
            raise ValidationError(self.message)
        except User.DoesNotExist:
            return self.username