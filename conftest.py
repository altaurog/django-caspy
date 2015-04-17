import os
import sys
from django.conf import settings

def pytest_configure():
    sys.path.append(os.path.join(os.path.dirname(__file__), 'tests'))
    test_settings = {
        'INSTALLED_APPS': (
            'caspy',
            'rest_framework',
            'testapp',
        ),

        'ROOT_URLCONF': 'caspy.urls',

        'DATABASES': {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },

        'USE_TZ': True,
        'MIDDLEWARE_CLASSES': [],
    }

    if os.getenv('USE_POSTGRESQL_DATABASE'):
        test_settings['DATABASES']['default'] = {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': os.getenv('PGDATABASE'),
                'USER': os.getenv('PGUSER'),
                'HOST': os.getenv('PGHOST'),
                'PASSWORD': os.getenv('PGPASSWORD'),
            }
    settings.configure(**test_settings)
