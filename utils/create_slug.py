import  string 
from random import SystemRandom

from django.utils.text import slugify


def random_letters(qtd=5):
    list_caracters = SystemRandom().choices(
        string.ascii_letters + string.digits,
        k=qtd
    )
    text = ''
    for i in list_caracters:
        
        text += i
    
    return text 


def slugify_new(text):
    return slugify(text) + '-' + random_letters()