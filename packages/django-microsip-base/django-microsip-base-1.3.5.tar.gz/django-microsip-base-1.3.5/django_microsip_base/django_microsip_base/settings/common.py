#encoding:utf-8
import django.contrib.humanize
# Identificando la ruta del proyecto
import os
import fdb
import sqlite3
import socket
from uuid import getnode as get_mac

def get_microsip_extra_apps(EXTRA_MODULES, is_dev= False):
    allowed_apps = []
    import importlib, sys
    EXTRA_APPS = []
    sic_password = os.getenv('SIC_PASSWORD')
    from microsip_api.core.crypt import EncoderSIC
    enc = EncoderSIC()
    if not is_dev:
        value = enc.decrypt(sic_password)
        allowed_apps = value.split('|')[1].split(',')
    
    for module in EXTRA_MODULES:
        if module in allowed_apps or is_dev:
            try:
                module_config = importlib.import_module(module+'.config')
            except ImportError as exc:
                sys.stderr.write("Error: failed to import settings module ({})".format(exc))
            else:
                module_settings = module_config.settings

                EXTRA_APPS.append({
                    'app': module,
                    'name': module_settings['name'],
                    'icon_class':module_settings['icon_class'],
                    'url':module_settings['url'],
                    'url_main_path':module_settings['url_main_path'],
                    'users':module_settings['users'],
                    }
                )

    MICROSIP_EXTRA_APPS = ()
    
    for microsip_app in EXTRA_APPS:
        MICROSIP_EXTRA_APPS += (microsip_app['app'],)

    return MICROSIP_EXTRA_APPS, EXTRA_APPS
    

EXTRA_INFO = {
    'ruta_datos_facturacion': 'C:\sat',
}

DJANGO_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.humanize',
    'autocomplete_light',
    'djcelery',
    'multiselectfield',
    'xhtml2pdf',
)

MICROSIP_MODULES = (
    'django_microsip_base.libs.models_base',
    'microsip_api.apps.config',
    'microsip_api.apps.metadatos',
    'microsip_api.apps.administrador',
    'django_microsip_base.apps.main',
)

# FORM_RENDERER = 'django.forms.renderers.DjangoTemplates'

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
print(BASE_DIR)
ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MICROSIP_DATOS_PATH = os.environ['MICROSIP_DATOS_PATH']
MANAGERS = ADMINS
DATABASE_ROUTERS = ['django_microsip_base.libs.databases_routers.MainRouter']
MICROSIP_DATABASES = {}
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME':  os.path.join(MICROSIP_DATOS_PATH, 'System' ,'U.sqlite3'),
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        'ATOMIC_REQUESTS': True,
    },
}
try:
    users_conn = sqlite3.connect(os.path.join(MICROSIP_DATOS_PATH, 'System' ,'U.sqlite3'))
    users_cur = users_conn.cursor()
    users_cur.execute('''SELECT * FROM auth_conexiondb''')
    conexiones_rows = users_cur.fetchall()
    users_conn.close()

    for conexion in conexiones_rows:
        
        conexion_id = conexion[0]
        conexion_id = "%02d" % conexion_id
        host = conexion[3]
        password = conexion[6]
        user = conexion[5]
        carpeta_datos = conexion[4]
        conexion_exitosa = True
        try:
            db= fdb.connect(host=host, user=user, password=password, database="%s\System\CONFIG.FDB"%carpeta_datos )
        except fdb.DatabaseError:
            conexion_exitosa = False
        else:
            cur = db.cursor()
            cur.execute("SELECT NOMBRE_CORTO FROM EMPRESAS")
            empresas_rows = cur.fetchall()
            db.close()
        
        if conexion_exitosa:

            DATABASES[ '%s-CONFIG'%conexion_id ] = {
                'ENGINE': 'firebird', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
                'NAME': '%s\System\CONFIG.FDB'% carpeta_datos,
                'USER': user,                      # Not used with sqlite3.
                'PASSWORD': password,                  # Not used with sqlite3.
                'HOST': host,                      # Set to empty string for localhost. Not used with sqlite3.
                'PORT': '3050',                      # Set to empty string for default. Not used with sqlite3.
                'OPTIONS' : {'charset':'ISO8859_1'},
                'ATOMIC_REQUESTS': True,
            }

            DATABASES[ '%s-METADATOS'%conexion_id ] = {
                'ENGINE': 'firebird', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
                'NAME': '%s\System\Metadatos.fdb'% carpeta_datos,
                'USER': user,                      # Not used with sqlite3.
                'PASSWORD': password,                  # Not used with sqlite3.
                'HOST': host,                      # Set to empty string for localhost. Not used with sqlite3.
                'PORT': '3050',                      # Set to empty string for default. Not used with sqlite3.
                'OPTIONS' : {'charset':'ISO8859_1'},
                'ATOMIC_REQUESTS': True,
            }

            for empresa in empresas_rows:                
                try:
                    name = '%s\%s.FDB'% (carpeta_datos, empresa[0])
                except UnicodeDecodeError:
                    pass
                else:
                    MICROSIP_DATABASES['%s-%s'%(conexion_id, empresa[0].replace(' ','_'))] = {
                        'ENGINE': 'firebird', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
                        'NAME': name,
                        'USER': user,                      # Not used with sqlite3.
                        'PASSWORD': password,                  # Not used with sqlite3.
                        'HOST': host,                      # Set to empty string for localhost. Not used with sqlite3.
                        'PORT': '3050',                      # Set to empty string for default. Not used with sqlite3.
                        'OPTIONS' : {'charset':'ISO8859_1'},
                        'ATOMIC_REQUESTS': True,
                    }

                    DATABASES['%s-%s'%(conexion_id, empresa[0].replace(' ','_'))] = {
                        'ENGINE': 'firebird', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
                        'NAME': name,
                        'USER': user,                      # Not used with sqlite3.
                        'PASSWORD': password,                  # Not used with sqlite3.
                        'HOST': host,                      # Set to empty string for localhost. Not used with sqlite3.
                        'PORT': '3050',                      # Set to empty string for default. Not used with sqlite3.
                        'OPTIONS' : {'charset':'ISO8859_1'},
                        'ATOMIC_REQUESTS': True,
                    }

            
except Exception as e:
    print( "Error %s:" % e.args[0])

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Mazatlan'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'es-mx'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
#MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# os.path.join(BASE_DIR,'media' 
# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"

import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    s.connect(('google.com', 0))
except:
    ip  = '127.0.0.1'
else:
    ip = s.getsockname()[0]
nombre_equipo = socket.gethostname()
direccion_equipo = socket.gethostbyname(nombre_equipo)

ALLOWED_HOSTS = [ip,'127.0.0.1']

MEDIA_URL = '/media/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

PDF = os.path.join(BASE_DIR, 'static')

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'dajaxice.finders.DajaxiceFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',

)


# Make this unique, and don't share it with anybody.
SECRET_KEY = '95q^soklxvniuk3(numzeb4-kbq2&h!iu1i195vj^xk2znx9ms'

# CACHES = {
#     # … default cache config and others
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis://127.0.0.1:6379/1",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         }
#     },
#     "select2": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis://127.0.0.1:6379/2",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         }
#     }
# }

# # Tell select2 which cache configuration to use:
# SELECT2_CACHE_BACKEND = "select2"

MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'microsip_api.comun.middleware.CustomerMiddleware',
    # 'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.cache.CacheMiddleware',
    # 'django.middleware.transaction.TransactionMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',
    #'minidetector2.Middleware',
    
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'django_microsip_base.wsgi.application'

# List of callables that know how to import templates from various sources.
# TEMPLATE_LOADERS = (
#     'django.template.loaders.filesystem.Loader',
#     'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
# )
# TEMPLATE_DIRS = (
#     # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
#     # Always use forward slashes, even on Windows.
#     # Don't forget to use absolute paths, not relative paths.
#     (BASE_DIR + '/templates'),
# )

# TEMPLATE_CONTEXT_PROCESSORS = (

# )
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # insert your TEMPLATE_DIRS here
            (BASE_DIR + '/templates'),
        ],
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                # 'django.contrib.auth.context_processors.auth',
                # 'django.core.context_processors.debug',
                # 'django.core.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.request',
                # 'django.contrib.messages.context_processors.messages',
                'django_microsip_base.context_processors.menu',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                # insert your TEMPLATE_LOADERS here
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                # 'django.template.loaders.eggs.Loader',
            ]
        },
    },
]


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

#Configuraciones para enviar mensajes usando gmail
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'remitente@gmail.com'
EMAIL_HOST_PASSWORD = 'clavedelcorreo'
EMAIL_PORT = 587
