"""
Django settings for Data project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-_1mkd=(vx!!ra%(!t@e=vo6j0o-71bk*3s5&f*8vj%b#q9^)n1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'datapp.apps',
    'datapp.apps.DatappConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'utils.middle.AuthMiddleware'
]

ROOT_URLCONF = 'Data.urls'

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


WSGI_APPLICATION = 'Data.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(BASE_DIR / 'db.sqlite3'),  # 确保这里使用 str() 转换
    }
}

# Mysql数据库配置
# DATABASES = {'default':
#              {
#             'ENGINE': 'django.db.backends.mysql',
#               'NAME': 'your_database_name',
#                 'USER': 'your_mysql_user',
#                 'PASSWORD': 'your_mysql_password',
#                 'HOST': 'localhost',
#                 'PORT': '3306',
#                 }
#     }

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LANGUAGE_CODE = 'zh-hans'

# 换成自己Logo链接
SIMPLEUI_LOGO ='https://ps.ssl.qhimg.com/t019d46d269c46c25e9.jpg'

SIMPLEUI_HOME_INFO = False


SIMPLEUI_HOME_ACTION = False # 去掉"最近动作"


SIMPLEUI_CONFIG = {
    'system_keep': True,
    'menu_display': ['首页','可视化','用户管理'],      # 开启排序和过滤功能, 不填此字段为默认排序和全部显示, 空列表[] 为全部不显示.
    'dynamic': True,  # 设置是否开启动态菜单, 默认为False. 如果开启, 则会在每次用户登陆时动态展示菜单内容
    'menus': [
        {
            'name': '可视化',
            'icon': 'fa-fw fa fa-leaf',
            'models': [{
                'name': '文章报表',
                'icon': 'far fa-surprise',
                'url': 'https://www.baidu.com'
            }]
        },
        {
            'name': '用户管理',
            'icon': 'fa-fw fa fa-user',
            'url': '/login/'
        },
        {
            'name': '图书页面',
            'icon': 'fa-fw fa fa-user',
            'url': '/books/'
        }
    ]
}
