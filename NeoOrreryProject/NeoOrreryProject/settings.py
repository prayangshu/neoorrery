import os
from pathlib import Path
import django_heroku
import dj_database_url
from dotenv import load_dotenv

# Load environment variables from .env file (for local development)
load_dotenv()

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Secret key and debug setting loaded from environment variables for better security
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-7vb%lb!y@9gdtc6cm#&!0fpq%zfv8&19af8n4dg^+84_1cc7c!')

# Set DEBUG to False in production
DEBUG = os.getenv('DEBUG', 'True') == 'True'

# Hosts allowed to access the project, including Heroku app domain
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1,localhost,neoorrery-292eed339cfc.herokuapp.com').split(',')

# Installed apps, including the orrery app
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'orrery',
]

# Only include sslserver in development mode
if DEBUG:
    INSTALLED_APPS += ['sslserver']

# Middleware configuration, including WhiteNoise for static files
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # WhiteNoise middleware for static files
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
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Optionally use templates directory
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

# Database configuration (using PostgreSQL for Heroku, fallback to SQLite for local)
DATABASES = {
    'default': dj_database_url.config(default=f'sqlite:///{BASE_DIR}/db.sqlite3', conn_max_age=600)
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
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', 'mail@prayangshu.com')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', 'PrayangshUUU73@XD')

# Set default from email for sending
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Default auto field for primary keys
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Security settings for production
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

if not DEBUG:
    # Use secure cookies
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    # Redirect all HTTP traffic to HTTPS
    SECURE_SSL_REDIRECT = True

    # Use HTTP Strict Transport Security (HSTS) for 1 year
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    # Prevent the browser from guessing file types
    SECURE_CONTENT_TYPE_NOSNIFF = True

# Configure Django App for Heroku
django_heroku.settings(locals())
