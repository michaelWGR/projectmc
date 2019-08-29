# -*- coding:utf-8 -*-
"""
Django settings for aiResource project.

Generated by 'django-admin startproject' using Django 1.9.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# import djcelery

# djcelery.setup_loader()
# BROKER_URL = 'amqp://guest@localhost//'
# CELERY_RESULT_BACKEND = 'amqp://guest@localhost//'
#
# CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*8=inr-=jgp&!qln_)g6$(96hrb69&_2cd@#$d#n($c98oolri'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'djcelery',
    'management'
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'aiResource.urls'

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

WSGI_APPLICATION = 'aiResource.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        # online
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ai_test',
        'USER': 'michael',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '',
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'zh-hans'
DEFAULT_CHARSET = 'utf-8'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/assets/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'assets'),
)
PEM_PATH = os.path.join(BASE_DIR, "management", "third_party", "pem")
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'log', 'aiResource.log'),
            'when': 'D',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'management': {  # 每一个APP都需要配置，如需全局配置则添加 'root' 项（与handlers项同级）
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
    'formatters': {
        'verbose': {
            'format': '[%(levelname)s] [%(asctime)s] [%(module)s.%(funcName)s] %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    # 'root' {} root日志配置
}

KSYUN_SETTING = {
    'access_key': 'AKLTH4xlrvBdR-u9TXGAhsowKA',
    'secret_key': 'OG5kl7Pl0WZoOuRLfDrF1ZmFHkdhMN9t+SlCcXjoGjQH/178feflL/rKAqdbfFwd4w=='
}

ALIYUN_SETTING = {
    "access_key_id": "LTAIcMmmTfSs7rrH",
    "access_key_secret": "MV0tDj5rAr6Y0gWFTDwMl1orViOVyn",
    "domain": "green.cn-shanghai.aliyuncs.com",
    "server": "cn-shanghai",
}

BAIDUCLOUD_SETTING = {
    'app_id': '11612348',
    'secret_id': '8wQ9G53im8RgZTebibkLsLg6',
    'secret_key': 'YHrtk3LBbqox5TMQjCCwkCr31XnhjpHv'
}

TXCLOUD_SETTING = {
    'app_id': '1257170265',
    'secret_id': 'AKIDBLTUN88KmFZizBeyb6Rj5gKbieRq9W1O',
    'secret_key': 'Ut7B6DF6pMk2FPSK6lIetzwlQ8vrlaHr'

}

TUPUTECH_SETTING = {
    "secret_id": {"porn": '5b582d8393c70fabecff93a7', "ocr": '5b5aca05878b01abf107e3c9'},
    "private_key_path": os.path.join(PEM_PATH, 'tupu_rsa_private_key.pem')
}

YYAIIMAGE_SETTING = {
    "secret_id": "91ffeffb337b20e743c588ff84e13711",
    "private_key_path": os.path.join(PEM_PATH, 'yy_rsa_private_key.pem')
}

# Local settings
try:
    # Import the configuration settings file - REPLACE projectname with your project
    config_module = __import__('aiResource.dev_settings', globals(), locals(), 'dev_settings')
    # Load the config settings properties into the local scope.
    for setting in dir(config_module):
        if setting == setting.upper():
            locals()[setting] = getattr(config_module, setting)
except ImportError, e:
    # Ignore
    pass