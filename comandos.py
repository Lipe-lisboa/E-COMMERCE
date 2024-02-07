# django-admin startproject project .  -> criar a pasta do projeto


# cd djangoapp 
# py manage.py startapp blog

# py djangoapp/manage.py runserver -> subir o servidor

# contro + C -> para o servidor

# settings.py -> lugar onde configura o projeto

# python manage.py collectstatic

#pip install whitenoise


#   STATICFILES_DIRS = [
#       BASE_DIR/ 'base_static',
#   ]


#    'DIRS': [  
#        BASE_DIR / 'base_templates'
#        ],


# pasta dotenv_files: variaveis de ambiente

# arquivo .dockerignore: coisas para o docker ignorar (pegar no google)

# precisa criar um arquivo urls.py em cada app

# a views do app precisa estar ligada a url do app. preciso ligara  aurls do app
# com a urls do projeto

#precisa registrar os models no admin

'''
http://127.0.0.1:8000/admin/

Migrando a base de dados do Django

python manage.py makemigrations  (execultar sempre que mudar algo no models)
python manage.py migrate

Criando e modificando a senha de um super usuário Django


python manage.py createsuperuser
python manage.py changepassword USERNAME

'''

'''
py manage.py shell 
from contact.models import Contact
Contact

c = Contact(first_name = 'Miguel')
c
c.save()
c.last_name = 'Oliveira' 
c.save()
c.delete()

c = Contact.objects.get(id = 1) -> apenas um valor


c = Contact.objects.all() -> varios valores=
for contact in c: contact.first_name

c = Contact.objects.all().order_by('-id') 
c


c = Contact.objects.filter(id=4) 
c
for contact in c: contact.phone 
c = Contact.objects.create(first_name='Edu', last_name='Vieira')
c
'''

'''
from django.contrib.auth.models import User 
user = User.objects.create_user(username='usuario',password='123')
'''