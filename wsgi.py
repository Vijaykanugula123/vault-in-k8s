import os
import hvac
from pathlib import Path

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = 'django-insecure--rtivbmobau&7#14u8tk3-uhs)i5)vdfqx(t0)i!gg(7p_r82&'

# ----- Constants -----
VAULT_URL = os.environ.get("VAULT_URL", "http://vault.vault-devsecops.svc.cluster.local:8200")
VAULT_ROLE = os.environ.get("VAULT_ROLE", "myapp-role")
VAULT_PATH = "myapp/config"
TOKEN_FILE = "/var/run/secrets/kubernetes.io/serviceaccount/token"

# ----- Function to Load Secrets from Vault -----
def load_secrets_from_vault():
    try:
        with open(TOKEN_FILE, "r") as f:
            jwt = f.read().strip()

        client = hvac.Client(url=VAULT_URL)
        client.auth.kubernetes.login(role=VAULT_ROLE, jwt=jwt)

        if not client.is_authenticated():
            raise Exception("Vault authentication failed")

        response = client.secrets.kv.v2.read_secret_version(path=VAULT_PATH)
        return response['data']['data']
    except Exception as e:
        print(f"Failed to load secrets from Vault: {e}")
        return {}

# ----- Load Initial Secrets -----
SECRETS = load_secrets_from_vault()

# ----- Override os.getenv -----
class SecretEnvFallback:
    def __init__(self, secrets):
        self.secrets = secrets

    def getenv(self, key, default=None):
        return self.secrets.get(key, os.environ.get(key, default))

# Override os.getenv globally
os.getenv = SecretEnvFallback(SECRETS).getenv

# ----- Django Settings -----

# SECURITY WARNING: use a real secret key in production!
DEBUG = True  # Turn off in production!

ALLOWED_HOSTS = ['*']

# Database configuration using Vault secrets
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
        'CONN_MAX_AGE': 0,  # Disable persistent connections
    }
}


DATABASES1 = {
    'default1': {
        'key1': {
            'key2':{
                'key3':{
                    'key4':{
                        'key5': os.getenv('vijay')
                    }
                }
            }
        }
    }
}
# Optional app-specific secrets from Vault
MY_SEC_URL = os.getenv("mySecUrl")
MY_SEC_PASS = os.getenv("mySecPass")

# Optional: debug logging
print("✅ Initial Vault secrets loaded:")
print("DB_HOST:", os.getenv("DB_HOST"))
print("DB_USER:", os.getenv("DB_USER"))
print("MY_SEC_URL:", MY_SEC_URL)

# Application definition
INSTALLED_APPS = [
    'myapp',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'my_django_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'my_django_project.wsgi.application'

# Password validation
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
