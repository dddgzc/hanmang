"""
Django settings for hanmang project.

Generated by 'django-admin startproject' using Django 2.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import datetime

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'd-nb301^z&i-0db4-h##ucf_8a0w^$&+wt3_kc&$rcrg#t+a3_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.courses.apps.CoursesConfig',
    'apps.users.apps.UsersConfig',
    'apps.organizations.apps.OrganizationsConfig',
    'apps.operations.apps.OperationsConfig',
    'crispy_forms',
    'xadmin.apps.XAdminConfig',
    'DjangoUeditor',
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

ROOT_URLCONF = 'hanmang.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'hanmang.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db_hanmang',
        'USER':'root',
        'PASSWORD':'18996122619',
        'HOST':'148.70.169.113',
        'OPTIONS':{'charset':'utf8mb4'},
    }
}

## 配置redis
# CACHES = {
#     'default':{
#         "BACKEND":"django_redis.cache.RedisCache",
#         "LOCATION":"redis://148.70.169.113/1",
#         "OPTIONS":{
#             'CLIENT_CLASS':'django_redis.client.DefaultClient',
#         }
#     }
# }
# 配置外部可访问
ALLOWED_HOSTS = [
    '0.0.0.0',
    '192.168.8.114',
    '192.168.80.128',
    '192.168.80.55',
    '192.168.43.114',
    '192.168.0.7',
    '127.0.0.1'
]

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

APPEND_SLASH=False

# LifeJoke 的小程序APPID和APPKEY
# appid
APP_ID = 'wxe6851ea0c162e8cf'
# appkey
APP_KEY = 'fd9f85627742e69506f8bc7bd07a2e6b'
#jwt 配置

# 寒芒的商户key 这是的要重新写
Mch_key = '323423sfadsfasdf'
# 微信支付访问接口
order_url = 'https://api.mch.weixin.qq.com/pay/unifiedorder'

REST_FRAMEWORK = {
'DEFAULT_AUTHENTICATION_CLASSES':(
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7)
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = "users.UserProfile"

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR,'static'),
]