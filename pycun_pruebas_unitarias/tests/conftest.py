import os
import pytest
import django
from django.conf import settings

# Establece la configuración de Django antes de que cualquier prueba se ejecute
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pycun_pruebas_unitarias.settings')


@pytest.fixture(scope='session')
def django_db_setup():
    # Configuración de la base de datos para las pruebas
    settings.DEBUG = False
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',  # Base de datos en memoria para pruebas rápidas
    }
    # Inicializa Django
    django.setup()
