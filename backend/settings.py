import os
from pathlib import Path
import environ
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize environment variables
env = environ.Env(
    DEBUG=(bool, False),
)

# Read .env file
environ.Env.read_env(BASE_DIR / '.env')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY', default='django-insecure-s$uo5(*c7j*a2qstb3xbx$(zwn^2%+^+08yly_w=m+7r+yppo%')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=True)

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'django.contrib.sites',  # Required for allauth
	'rest_framework',
	'rest_framework_simplejwt',
	'drf_spectacular',
	'corsheaders',
	'allauth',
	'allauth.account',
	'allauth.socialaccount',
	'allauth.socialaccount.providers.google',
	'allauth.socialaccount.providers.facebook',
	'allauth.socialaccount.providers.instagram',
	'allauth.socialaccount.providers.github',
	'allauth.socialaccount.providers.twitter',
	'api',
]

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'corsheaders.middleware.CorsMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'backend.urls'

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
			],
		},
	},
]

WSGI_APPLICATION = 'backend.wsgi.application'


# Database Configuration
# Use PostgreSQL in production, SQLite for development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME', default='rupixai_db'),
        'USER': env('DB_USER', default='rupixai_user'),
        'PASSWORD': env('DB_PASSWORD', default='rupixai_password'),
        'HOST': env('DB_HOST', default='localhost'),
        'PORT': env('DB_PORT', default='5432'),
    }
}

# Fallback to SQLite for development if PostgreSQL is not available
if env.bool('USE_SQLITE', default=False):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# Simple JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
}

# drf-spectacular
SPECTACULAR_SETTINGS = {
    'TITLE': 'RupixAI API',
    'DESCRIPTION': 'AI Image Generation Platform API',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

# CORS settings
CORS_ALLOW_ALL_ORIGINS = env.bool('CORS_ALLOW_ALL_ORIGINS', default=True)
CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=['http://localhost:3000', 'http://127.0.0.1:3000'])

# API Keys
OPENAI_API_KEY = env('OPENAI_API_KEY', default='')
GEMINI_API_KEY = env('GEMINI_API_KEY', default='')

# Payment Gateway API Keys
KHALTI_SECRET_KEY = env('KHALTI_SECRET_KEY', default='')
ESEWA_SECRET_KEY = env('ESEWA_SECRET_KEY', default='')
STRIPE_SECRET_KEY = env('STRIPE_SECRET_KEY', default='')
RAZORPAY_SECRET_KEY = env('RAZORPAY_SECRET_KEY', default='')
BINANCE_API_KEY = env('BINANCE_API_KEY', default='')
BINANCE_SECRET_KEY = env('BINANCE_SECRET_KEY', default='')

# Frontend URL for password reset links
FRONTEND_URL = env('FRONTEND_URL', default='http://localhost:3000')

# Email configuration (for password reset)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # For development
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # For production
EMAIL_HOST = env('EMAIL_HOST', default='')
EMAIL_PORT = env('EMAIL_PORT', default=587)
EMAIL_USE_TLS = env('EMAIL_USE_TLS', default=True)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='noreply@rupixai.com')

# Django Allauth Configuration
SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

ACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'username'
ACCOUNT_UNIQUE_EMAIL = True

# Social Account Settings
SOCIALACCOUNT_EMAIL_REQUIRED = False
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_AUTO_SIGNUP = True

# Social Provider Settings
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'OAUTH_PKCE_ENABLED': True,
    },
    'facebook': {
        'METHOD': 'oauth2',
        'SDK_URL': '//connect.facebook.net/{locale}/sdk.js',
        'SCOPE': ['email', 'public_profile'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'INIT_PARAMS': {'cookie': True},
        'FIELDS': [
            'id',
            'first_name',
            'last_name',
            'middle_name',
            'name',
            'name_format',
            'picture',
            'short_name'
        ],
        'EXCHANGE_TOKEN': True,
        'LOCALE_FUNC': 'path.to.callable',
        'VERIFIED_EMAIL': False,
        'VERSION': 'v7.0',
    },
    'instagram': {
        'SCOPE': ['user_profile'],
    },
    'github': {
        'SCOPE': [
            'user',
            'repo',
            'read:org',
        ],
    },
    'twitter': {
        'SCOPE': ['read'],
    },
}

# OAuth Credentials (set these in your .env file)
GOOGLE_OAUTH2_CLIENT_ID = env('GOOGLE_OAUTH2_CLIENT_ID', default='')
GOOGLE_OAUTH2_CLIENT_SECRET = env('GOOGLE_OAUTH2_CLIENT_SECRET', default='')

FACEBOOK_APP_ID = env('FACEBOOK_APP_ID', default='')
FACEBOOK_APP_SECRET = env('FACEBOOK_APP_SECRET', default='')

INSTAGRAM_CLIENT_ID = env('INSTAGRAM_CLIENT_ID', default='')
INSTAGRAM_CLIENT_SECRET = env('INSTAGRAM_CLIENT_SECRET', default='')

GITHUB_CLIENT_ID = env('GITHUB_CLIENT_ID', default='')
GITHUB_CLIENT_SECRET = env('GITHUB_CLIENT_SECRET', default='')

TWITTER_CLIENT_ID = env('TWITTER_CLIENT_ID', default='')
TWITTER_CLIENT_SECRET = env('TWITTER_CLIENT_SECRET', default='')

# Database Connection Pooling (for production)
if not DEBUG:
    DATABASES['default']['CONN_MAX_AGE'] = 600

# Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'api': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
