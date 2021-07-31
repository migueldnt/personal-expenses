from django.core.management.base import BaseCommand
import os
from django.contrib.auth.models import User
#from administracion.models import Empleado


class Command(BaseCommand):
    def handle(self, **options):
        user = os.environ["ADMIN_USER"]
        passw = os.environ["ADMIN_PASS"]
        email="admin@example.com"
        #solo si no existe el usuario agregar
        existe=User.objects.filter(username=user).exists()
        if existe:
            print("superusuario ya existe")
        else:
            the_user=User.objects.create_superuser(user, email, passw,first_name=str(user).capitalize())
            print("superusuario creado")
            
