from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-j9are96$$p*6)=vasi6t$wn02sqatxy0zwm(b$psceklbt=zr^'

RECAPTCHA_PUBLIC_KEY = '66LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
RECAPTCHA_PRIVATE_KEY = '6Ldn8mwrAAAAANAFZFPU2m6zJvlNx15lAWHdrpQy'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# LOGIN_URL = '/login/'
# LOGIN_REDIRECT_URL = '/'# Ou l'URL vers laquelle rediriger après une connexion réussie

# Application definition


# Configuration de la page Admin Générer avec JAZZMIN
JAZZMIN_SETTINGS = {
    "site_title": "PANNEAUTAGE",           # Nom dans l'onglet navigateur
    "site_brand": "Panneautage",                 # Nom en haut à gauche
    "site_logo": "image/BD_ADRESSAGE.png",     # Logo dans ton static
    "site_icon": "image/icon_logo.png",    # Favicon (dans ton static)

    # Sidebar
    "copyright": "BNETD Centrale d'Adressage © 2025",

    # Icônes des apps
    "icons": {
        "myapp.Voie": "fas fa-road",         # Icône route pour Voie
        "myapp.Suggestion": "fas fa-lightbulb",  # Icône idée pour Suggestion
        "auth": "fas fa-users",              # Icône utilisateurs
    },

    # Réorganisation du menu
    "order_with_respect_to": [
        "myapp",   # Ton app en premier
        "auth",    # Puis Auth en dessous
    ],

}

JAZZMIN_UI_TWEAKS = {
    "theme": "cosmo",
}

INSTALLED_APPS = [
    'jazzmin',  # Application d'un autre theme Admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp',  # Application personnalisée créée pour le projet
    'custom_admin',  # Application admin du projet
    'street_views',  
]


LOGIN_URL = '/p_bnetd25/login/'
LOGIN_REDIRECT_URL = '/p_bnetd25/dashboard/'
LOGOUT_REDIRECT_URL = '/p_bnetd25/login/'



# AUTH_USER_MODEL = 'myapp.customuser' 

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'myapp.context_processors.publicite_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'myproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql', # Indique que le moteur utilisé est PostgreSQL
        'NAME': 'db_qrcode', # Nom de la base de données PostgreSQL
        'USER': 'postgres', # Nom d'utilisateur pour se connecter à PostgreSQL
        'PASSWORD': 'yanick',
        'HOST': 'localhost',  # l'adresse de votre serveur PostgreSQL
        'PORT': '5432',  # le port par défaut pour PostgreSQL
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators



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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# BASE_URL = 'http://127.0.0.1:8000'  # À adapter

STATIC_URL = 'static/'  # Spécifie l'URL de base pour accéder aux fichiers statiques (images)
MEDIA_URL = '/media/'  # Spécifie l'URL de base pour accéder aux fichiers médias  
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Définit le répertoire sur le disque où seront stockés les fichiers médias


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
