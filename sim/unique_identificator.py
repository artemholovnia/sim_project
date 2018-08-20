import random
import string

def create_identificator(len):
    return ''.join([random.choice((string.digits+string.ascii_lowercase+string.ascii_uppercase)) for itter in range(len)])