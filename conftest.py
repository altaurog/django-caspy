import os
import sys
from django.conf import settings

def pytest_configure():
    sys.path.append(os.path.join(os.path.dirname(__file__), 'tests'))
    settings.configure(
        INSTALLED_APPS = (
            'caspy',
            'rest_framework',
            'testapp',
        ),

        ROOT_URLCONF = 'caspy.urls',

        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },

        USE_TZ = True,
    )
