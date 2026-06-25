from pathlib import Path
from datetime import timedelta
from celery.schedules import crontab
from dotenv import load_dotenv
import os

load_dotenv()
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
}


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")
api_key = os.getenv("API_KEY_SECRET")

if not api_key:
    raise ValueError("API_KEY_SECRET environment variable is missing")

API_KEY_SECRET = api_key.encode()


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "False") == "True"


ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [

    # web socket
    "daphne",
    "channels",

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # DRF
    "rest_framework",
    "drf_yasg",
    "django_celery_beat",
    # APPS
    "accounts",
    "tasks",
    
]

MIDDLEWARE = [
    "main.middleware.ApiExceptionMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
]

ROOT_URLCONF = 'main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'main.wsgi.application'

ASGI_APPLICATION = "main.asgi.application"

# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE ="Asia/Kolkata"

USE_I18N = True

USE_TZ = True


AUTH_USER_MODEL = "accounts.User"


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/



# Static Files
STATIC_URL = '/static/'

STATICFILES_DIRS = [

    BASE_DIR / "static"

]

# Rest framework authentication
REST_FRAMEWORK = {

    "DEFAULT_AUTHENTICATION_CLASSES": (
        "accounts.authentication.APIKeyAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication", 
        
         
    ),  
    "DEFAULT_RENDERER_CLASSES": [
        "main.renderers.CustomRenderer",
    ],
    "EXCEPTION_HANDLER": "main.exceptions.custom_exception_handler"
}



# Celery setting
CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "Asia/Kolkata"


# Email setting
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = os.getenv("EMAIL_HOST_USER")



# Celery Beat setting
CELERY_BEAT_SCHEDULE = {

        "daily-task-reminder": {

            "task": "tasks.tasks.daily_task_reminder",
            "schedule": crontab(hour=9, minute=0),
        },

        "mark-overdue-every-day": {

                "task": "tasks.tasks.mark_overdue_tasks",
                "schedule": crontab(hour=6, minute=0),
        },
}


SWAGGER_SETTINGS = {
    "USE_SESSION_AUTH": False,

    "SECURITY_DEFINITIONS": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header"
        }
    }
}




CHANNEL_LAYERS = {
    "default": {
        "BACKEND":
        "channels.layers.InMemoryChannelLayer"
    }
}


