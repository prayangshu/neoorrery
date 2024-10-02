import os
from pathlib import Path
from celery.schedules import crontab

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Secret key and debug setting loaded from environment variables for better security
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-7vb%lb!y@9gdtc6cm#&!0fpq%zfv8&19af8n4dg^+84_1cc7c!')

# Set DEBUG to False in production
DEBUG = os.getenv('DEBUG', 'True') == 'True'

# Hosts allowed to access the project
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1,localhost,neoorrery-13c972087676.herokuapp.com').split(',')

# Installed apps, including Celery, Celery Beat, and the orrery app
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'orrery',
    'django_celery_beat',
    'tinymce',  # Use TinyMCE
]

# Middleware configuration
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Added whitenoise middleware for static file handling
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URL configuration
ROOT_URLCONF = 'NeoOrreryProject.urls'

# Templates configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # Specify template directories here if needed
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

# WSGI application configuration
WSGI_APPLICATION = 'NeoOrreryProject.wsgi.application'

# Database configuration (SQLite by default)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation settings
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Localization settings
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images) configuration
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'orrery/static']  # Directory for development static files
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Directory for production static files after collectstatic

# Add Whitenoise to handle static files in production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files (user-uploaded content)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Authentication settings
LOGIN_URL = '/login/'  # Set login URL to /login/
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Email configuration for SMTP (Hostinger)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.hostinger.com'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', 'no-reply@neoorrery.space')  # Updated email
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', 'NASASPACE2024@neo')  # Updated password

# Set default from email for sending
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Default auto field for primary keys
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Security settings
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# Additional security settings for production
if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000  # Enforce HTTPS for one year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True

# Celery Configuration
CELERY_BROKER_URL = 'redis://localhost:6379/0'  # Redis as a message broker
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'

# Celery Task Results Backend (optional, if you need to track task results)
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

# Timezone for Celery
CELERY_TIMEZONE = 'UTC'

# Celery task serializer
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_SERIALIZER = 'json'

# Celery beat schedule
CELERY_BEAT_SCHEDULE = {
    'fetch-nasa-data-every-6-hours': {
        'task': 'orrery.tasks.fetch_nasa_data_task',
        'schedule': crontab(minute=0, hour='*/6'),  # Run every 6 hours
    },
    'update-real-time-close-approaches-every-30-minutes': {
        'task': 'orrery.tasks.update_real_time_close_approaches',
        'schedule': crontab(minute='*/30'),  # Run every 30 minutes
    },
}

# Disable SSL verification for development if necessary
if DEBUG:
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context
