from pathlib import Path

# BASE_DIR = C:\Users\...\EduCongo
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'dev-secret-change-en-prod'
DEBUG = True # True = on voit les erreurs, en prod on met False
ALLOWED_HOSTS = []

# Nos briques. On a ajouté nos 4 apps.
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',   # 01 Connexion
    'scolarite',  # 03 Élèves
    'finance',    # 09 Frais
    'core',       # 02 Dashboard
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware', # Sécurité exigée p.19 cahier
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

ROOT_URLCONF = 'educongo.urls'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'templates'], # On dit à Django où sont nos HTML
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],
    },
}]

WSGI_APPLICATION = 'educongo.wsgi.application'

# Base vide au début. Normal. Les chiffres du cahier (1248, 77.7%) apparaîtront quand tu ajouteras des données.
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3'}}

# TRÈS IMPORTANT : On utilise NOTRE User, pas celui de Django. On doit le faire avant le premier migrate.
AUTH_USER_MODEL = 'accounts.User'

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Brazzaville'
USE_TZ = True

# STATICS - Norme industrie : séparé
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static'] # Notre dossier css/js/images
MEDIA_URL = '/media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_URL = '/connexion/'