# -*- coding: utf-8 -*-

import os
ROOT = os.path.abspath(os.path.dirname(__file__))
path = lambda *args: os.path.join(ROOT, *args)

DEBUG = True
APPEND_SLASH = False
TEMPLATE_DEBUG = DEBUG
THUMBNAIL_DEBUG = False
ADMINS = (
    (u'Никоненко Илья',  'iv@simplemedia.ru'),
    (u'Грин Тёма',  'tema@simplemedia.ru'),
    )

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mirt',
        'USER': 'mirt',
        'PASSWORD': 'mirt',
        'HOST': 'localhost',
        'PORT': '',
        }
}

TIME_ZONE = 'Asia/Yekaterinburg'
LANGUAGE_CODE = 'ru'

LANGUAGES = (
    ('ru', 'Russian'),
)

SITE_ID = 1

USE_I18N = True
USE_L10N = True
ALLOWED_HOSTS = [
    '.simplemedia.ru', # Allow domain and subdomains
    '.simplemedia.ru.', # Also allow FQDN and subdomains
]

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(PROJECT_ROOT, '..')
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = STATIC_URL + 'grappelli/'

STATICFILES_DIRS = ()

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

SECRET_KEY = '*ywveerf_(v1v7bcx0!&x=8%1g$(ky&b-28+#c#z7chrm3x$ruidc'
SESSION_COOKIE_AGE = 365 * 24 * 60 * 60

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.static',

)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'message.middleware.MessageMiddleware',
    'message.middleware.MailMiddleware',
    'main.middleware.SimpleSystemMiddleware',
    'main.middleware.FlatpageFallbackMiddleware',
    'lastmoder.middleware.SimpleCacheControlMiddleware',
    )

ROOT_URLCONF = 'main.urls'

TEMPLATE_DIRS = ()
for root, dirs, files in os.walk(PROJECT_ROOT):
    if 'templates' in dirs: TEMPLATE_DIRS += (os.path.join(root, 'templates'),
    )

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.humanize',
    'sorl.thumbnail',
    'south',
)

THUMBNAIL_PRESERVE_FORMAT = True

# grappelli, dashboard & filebrowser
INSTALLED_APPS = ('grappelli',) + INSTALLED_APPS
INSTALLED_APPS = ('grappelli.dashboard',) + INSTALLED_APPS
GRAPPELLI_INDEX_DASHBOARD = 'main.dashboard.CustomIndexDashboard'

GRAPPELLI_ADMIN_TITLE = u'Мир тюнинга'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        # I always add this handler to facilitate separating loggings
        'log_file':{
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(ROOT, '../../log/django.log'),
            'maxBytes': '16777216', # 16megabytes
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'apps': { # I keep all my of apps under 'apps' folder, but you can also add them one by one, and this depends on how your virtualenv/paths are set
            'handlers': ['log_file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
    # you can also shortcut 'loggers' and just configure logging for EVERYTHING at once
    'root': {
        'handlers': ['console', 'mail_admins'],
        'level': 'INFO'
    },
}

# custom attrigutes for form elements
INSTALLED_APPS += ('widget_tweaks',)

INSTALLED_APPS += ('lastmoder',)

# mptt
INSTALLED_APPS += ('mptt',)
MPTT_USE_FEINCMS = True

# feincms
INSTALLED_APPS += ('feincms',)

# filebrowser
INSTALLED_APPS = ('filebrowser',) + INSTALLED_APPS
FILEBROWSER_DIRECTORY = 'uploads/'
FILEBROWSER_ADMIN_VERSIONS = None
FILEBROWSER_MAX_UPLOAD_SIZE = 1 * 1024 * 1024 * 1024


# tinymce
INSTALLED_APPS += ('tinymce',)
TINYMCE_JS_URL = STATIC_URL + 'tiny_mce/tiny_mce.js'
TINYMCE_FILEBROWSER = True
TINYMCE_DEFAULT_CONFIG = {
    'theme': 'advanced',
    'width': '90%',
    "content_css": "/media/css/style.css, http://fonts.googleapis.com/css?family=Roboto&subset=latin",
    'height': '500px',
    'plugins': 'spellchecker,pagebreak,style,layer,table,save,advhr,advimage,advlink,emotions,iespell,inlinepopups,'
               'insertdatetime,preview,media,searchreplace,print,contextmenu,paste,directionality,fullscreen,'
               'noneditable,visualchars,nonbreaking,xhtmlxtras,template',
    'theme_advanced_buttons1': 'save,newdocument,|,bold,italic,underline,strikethrough,|,justifyleft,justifycenter,'
                               'justifyright,justifyfull,|,styleselect,formatselect,fontselect,fontsizeselect',
    'theme_advanced_buttons2': 'cut,copy,paste,pastetext,pasteword,|,search,replace,|,bullist,numlist,|,outdent,indent,'
                               'blockquote,|,undo,redo,|,link,unlink,anchor,image,cleanup,help,code,|,insertdate,'
                               'inserttime,preview,|,forecolor,backcolor',
    'theme_advanced_buttons3': 'tablecontrols,|,hr,removeformat,visualaid,|,sub,sup,|,charmap,emotions,iespell,media,'
                               'advhr,|,print,|,ltr,rtl,|,fullscreen',
    'theme_advanced_buttons4': 'insertlayer,moveforward,movebackward,absolute,|,styleprops,spellchecker,|,cite,abbr,'
                               'acronym,del,ins,attribs,|,visualchars,nonbreaking,template,blockquote,pagebreak,|,'
                               'insertfile,insertimage',

    'theme_advanced_toolbar_location': 'top',
    'theme_advanced_toolbar_align': 'left',
    'theme_advanced_statusbar_location': 'bottom',
    'force_br_newlines' : 'true',
    'forced_root_block' : '',
    'force_p_newlines' : 'false',
    'extended_valid_elements' : 'iframe[name|src|framespacing|border|frameborder|scrolling|title|height|width],'
                                'object[declare|classid|codebase|data|type|codetype|archive|standby|height|width|'
                                'usemap|name|tabindex|align|border|hspace|vspace]',
}

# constance
INSTALLED_APPS += ('constance',)
INSTALLED_APPS += ('constance.backends.database',)

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP
TEMPLATE_CONTEXT_PROCESSORS += TCP
TEMPLATE_CONTEXT_PROCESSORS += ('constance.context_processors.config',)

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
CONSTANCE_CONFIG = {
    'DEFAULT_TITLE': (u'', u'Заголовок страниц по умолчанию'),
    'DEFAULT_KEYWORDS': (u'', u'Keywords по умолчанию'),
    'DEFAULT_DESCR': (u'', u'Description по умолчанию'),

    'MANAGER_EMAIL': (u'', u'e-mail, на который будут приходить сообщения с формы обратной связи (несколько адресов можно ввести через запятую)'),
    'ORDER_TO_EMAIL': (u'', u'e-mail, на который будут приходить сообщения о заказах (несколько адресов можно ввести через запятую)'),
    'ORDER_FROM_EMAIL': (u'', u'e-mail,с которого будут отправляться сообщения с о заказах'),
    'EMAIL_FROM': (u'', u'e-mail,с которого будут отправляться сообщения с формы обратной связи'),
    'EMAIL_EXCHANGE': (u'dev@simplemedia.ru,in@simplemedia.ru', u'e-mail на который будут приходить письма с отчётом обмена (несколько адресов можно ввести через запятую)'),

    'CATALOG_PRICE_RANGE': (u"10", u" % от цены товара, задаёт диапазон товаров, похожих по цене"),
    'CATALOG_PER_PAGE': (u"12",u"Товаров на странице"),

    'ANNOUNCES_PER_PAGE': (u"4", u"Анонсов в списке"),
    'ANNOUNCES_ON_MAIN': (u"2", u"Анонсов в на главной"),

    'NEWS_PER_PAGE': (u"4", u"Новостей в списке"),
    'NEWS_ON_MAIN': (u"2", u"Новостей на главной"),
    'ORDERS_ON_PAGE': (u"3", u"Заказов в истории на одной странице"),
    'PRODUCTS_ON_MAIN': (u"4", u"Товаров на главной"),
}


# pytils
INSTALLED_APPS += ('pytils',)


# installed apps
INSTALLED_APPS += (
    'announce',
    'flatpages',
    'simpleseo',
    'error_manag',
    'news',
    'message',
    'feedback',
    'placeholder',
    'services',
    'slider',
    'catalog',
    'order',
    'quick_links',
    'sorl.thumbnail',
    'watermarker',
    'data_exchange',
    'personal',

)

# Django_compressor (SASS+SCSS support)
INSTALLED_APPS += ('compressor',)

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = False
COMPRESS_OFFLINE_TIMEOUT = 31536000

COMPRESS_OUTPUT_DIR = "compressed"
COMPRESS_URL = MEDIA_URL
COMPRESS_ROOT = MEDIA_ROOT

COMPRESS_DATA_URI_MAX_SIZE = 32000 # 32 KB for IE8 support
COMPRESS_CSS_FILTERS = (
    'compressor.filters.cssmin.CSSMinFilter',
    'compressor.filters.datauri.CssDataUriFilter',
)

COMPRESS_JS_FILTERS = (
    'compressor.filters.jsmin.JSMinFilter',
)

COMPRESS_PRECOMPILERS = (
    ('text/x-sass', 'sass --compass {infile} {outfile}'),
    ('text/x-scss', 'scss --compass {infile} {outfile}'),
    ('text/coffeescript', '/usr/local/bin/coffee -b --compile --stdio'),
)

STATICFILES_FINDERS += (
    'compressor.finders.CompressorFinder',
)

LOGIN_URL = '/?auth=True'

EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_HOST_USER = 'noreply@mir-tuninga.com'
EMAIL_HOST_PASSWORD = 'Gegrby!23'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

DEFAULT_FROM_EMAIL = 'noreply@mir-tuninga.com'
SERVER_EMAIL = 'noreply@mir-tuninga.com'
# DEFAULT_FROM_EMAIL = 'info@simplemedia.ru'
# SERVER_EMAIL = 'info@simplemedia.ru'

# registration
AUTH_PROFILE_MODULE = "personal.UserProfile"
INSTALLED_APPS += ('registration',)
ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_OPEN = True


try:
    from local_settings import *
except ImportError:
    pass



from os.path import expanduser
#execfile(os.path.join(PROJECT_ROOT, 'local_settings.py'))
