"""
Django settings for the CivicTrack FS project.

This is configured for local development / hackathon demo use. See the
"Before you deploy" section of README.md for the changes to make before
running this in production (SECRET_KEY, DEBUG, ALLOWED_HOSTS, HTTPS,
database choice, etc.) — those are exactly the cybersecurity best
practices called for in the project brief.
"""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# For a real deployment, load this from an environment variable instead,
# e.g. `SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]`.
SECRET_KEY = "dev-only-secret-key-change-before-deploying-8f1c3d9e2b"

# SECURITY WARNING: don't run with DEBUG turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "issues",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "civictrack_fs.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "civictrack_fs.wsgi.application"

# Database
# Defaults to SQLite for zero-config local/hackathon use. Swap the ENGINE
# to postgresql for a production deployment, e.g.:
#
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": os.environ["DB_NAME"],
#         "USER": os.environ["DB_USER"],
#         "PASSWORD": os.environ["DB_PASSWORD"],
#         "HOST": os.environ.get("DB_HOST", "localhost"),
#         "PORT": os.environ.get("DB_PORT", "5432"),
#     }
# }
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

LANGUAGE_CODE = "en-za"
TIME_ZONE = "Africa/Johannesburg"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
# issues/static/ is picked up automatically by Django's AppDirectoriesFinder
# (no need to list it in STATICFILES_DIRS as well).
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- Cybersecurity best practices (see README for the full checklist) ---
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = False  # Django needs to read this one client-side for forms
X_FRAME_OPTIONS = "DENY"
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
# When you deploy behind HTTPS, also set:
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_SSL_REDIRECT = True
# SECURE_HSTS_SECONDS = 31536000

# Report photo uploads are capped in forms.py (ReportForm.clean_photo) —
# keep DATA_UPLOAD_MAX_MEMORY_SIZE aligned with that limit.
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
