from django.conf import settings

def pytest_configure():
    settings.configure(
        INSTALLED_APPS = (
            'caspy',
            'rest_framework',
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
