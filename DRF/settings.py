"""
Django settings for DRF project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from pathlib import Path
from datetime import timedelta


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-7t1e(n%e8(gstfv715a*hsnbh9^4f(vgf)k9kh9yo8yseydnz='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition
# APPEND_SLASH = False
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',


    'apps.student.apps.StudentConfig',
    'apps.req.apps.ReqConfig',
    'apps.sers.apps.SersConfig',
    'apps.demo.apps.DemoConfig',
    'rest_framework',
    'rest_framework_simplejwt',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'apps.demo.middleware.check_login_middleware.CheckLoginMiddleware',
]

ROOT_URLCONF = 'DRF.urls'

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

WSGI_APPLICATION = 'DRF.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        'ENGINE': 'dj_db_conn_pool.backends.mysql',
        'NAME': 'django-drf',  # 数据库名字
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',  # ip
        'PORT': 3306,
        'POOL_OPTIONS': {
            'POOL_SIZE': 10,  # 最小
            'MAX_OVERFLOW': 10,  # 在最小的基础上，还可以增加10个，即：最大20个。
            'RECYCLE': 24 * 60 * 60,  # 连接可以被重复用多久，超过会重新创建，-1表示永久。
            'TIMEOUT': 30,  # 池中没有连接最多等待的时间。
        },
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        # 设置全局权限模式，用户认证通过可访问
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 使用默认的认证类的认证方式
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),  # 访问令牌的有效时间
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),  # 刷新令牌的有效时间
    "ROTATE_REFRESH_TOKENS": False,  # 若为True，则刷新后新的refresh_token有更新的有效时间
    "BLACKLIST_AFTER_ROTATION": True,  # 若为True，刷新后的token将添加到黑名单中,
    "ALGORITHM": "HS256",  # 对称算法：HS256 HS384 HS512  非对称算法：RSA
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,  # if signing_key, verifying_key will be ignore.
    "AUDIENCE": None,
    "ISSUER": None,
    "AUTH_HEADER_TYPES": ("Bearer",),  # Authorization: Bearer <token>
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",  # if HTTP_X_ACCESS_TOKEN, X_ACCESS_TOKEN: Bearer <token>
    "USER_ID_FIELD": "id",  # 使用唯一不变的数据库字段,将包含在生成的令牌中以标识用户
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),   # default: access
    "TOKEN_TYPE_CLAIM": "token_type",         # 用于存储令牌唯一标识符的声明名称 value:"access","sliding","refresh"
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",     # 滑动令牌是既包含到期声明又包含刷新到期声明的令牌
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),       # 只要滑动令牌的到期声明中的时间戳未通过，就可以用来证明身份验证
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),  # path("token|refresh", TokenObtainSlidingView.as_view())
}

