from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1i*lto=kq+!efwd*qajbu&^qwtkyoc8hg29gtbpbkqt0to@$ga'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
allowed_hosts_string = os.environ.get("ALLOWED_HOSTS")
allowed_hosts = allowed_hosts_string.split(" ") if allowed_hosts_string else []
ALLOWED_HOSTS = allowed_hosts + ['maraccia-hvhp.onrender.com', 'localhost', '127.0.0.1']

# Application definition
INSTALLED_APPS = [
    'crispy_forms',
    'crispy_bootstrap4',
    'inventory.apps.InventoryConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # WhiteNoise middleware ekledik
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Bu satır mevcut
    'django.contrib.messages.middleware.MessageMiddleware',     # Bu satır mevcut
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'inventorySystem.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Template dosyalarının bulunduğu dizini ekleyin
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'inventorySystem.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'stockmanagement_12xr',
        'USER': 'stockmanagement_12xr_user',
        'PASSWORD': 'MmwPuEXysZCDyKa1J7DDKXepug2PVsAa',
        'HOST': 'dpg-cpl3tsq0si5c738fgbk0-a.oregon-postgres.render.com',
        'PORT': '5432',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',  # Projenizin kök dizinindeki "static" klasörü
]

STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Crispy forms
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Login URLs
LOGIN_REDIRECT_URL = "/inventory"
LOGIN_URL = "login"
