import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = "django-insecure-gf*3pqan1f$tw+li%b)h$tf(11rdf151oslqd#$d205jao-h!$"
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'accounts',
    'stocks',
    'ai',
    'subscriptions',
    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth.registration',
    'corsheaders',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

SITE_ID = 1

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}

REST_AUTH = {
    'USE_JWT': True,
    'JWT_AUTH_COOKIE': 'didim-auth',
    'JWT_AUTH_REFRESH_COOKIE': 'didim-refresh',
    'REGISTER_SERIALIZER': 'accounts.serializers.CustomRegisterSerializer',
    # 로그인 시 'email' 필드를 받도록 명시
    'LOGIN_SERIALIZER': 'dj_rest_auth.serializers.LoginSerializer',
    'USER_DETAILS_SERIALIZER': 'accounts.serializers.UserProfileSerializer',
}

ROOT_URLCONF = "DIDIM.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "DIDIM.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "accounts.User"

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]


ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_SIGNUP_FIELDS = {
    "email": {"required": True},
}

load_dotenv()
NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID", '')
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET", '')

SOCIALACCOUNT_PROVIDERS = {
    'naver': {
        'APP': {
            'client_id': NAVER_CLIENT_ID,
            'secret': NAVER_CLIENT_SECRET,
        }
    }
}
KRX_API_KEY = os.getenv('KRX_API_KEY')
GMS_API_KEY = os.getenv('GMS_API_KEY')

# 미디어 파일 설정(프로필 이미지 등)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# 토스페이먼츠 설정
TOSS_CLIENT_KEY = os.getenv('TOSS_CLIENT_KEY', '')
TOSS_SECRET_KEY = os.getenv('TOSS_SECRET_KEY', '')