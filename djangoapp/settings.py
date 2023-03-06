from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY='sdsd'
DEBUG = True
INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.staticfiles',
    'drf_yasg',
    'rest_framework',
    'api',
    'thewall'
]
ROOT_URLCONF = 'djangoapp.server'
STATIC_URL='boom/'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
    },
]

WSGI_APPLICATION = 'djangoapp.server.application'

DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "thewall",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "db",
        "PORT": 5432,
    }
}

