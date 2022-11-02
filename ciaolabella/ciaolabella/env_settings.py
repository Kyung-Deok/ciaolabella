import os
from datetime import date
import logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] : %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'file': {
            'level': 'INFO',
            'encoding': 'utf-8',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': f'/home/ubuntu/ciaolabella2/logs/user/{date.today().isoformat()}.log',
            # 'maxBytes': 1024*1024*5,  # 5 MB
            'formatter': 'standard',
            'backupCount': 5,
        },
        'errors': {
            'encoding': 'utf-8',
            'level': 'ERROR',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': f'/home/ubuntu/webserver_logs/error/{date.today().isoformat()}.log',
            'maxBytes': 1024*1024*5,  # 5 MB
            'formatter': 'standard',
            'backupCount': 5,
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
    },
    'loggers': {

    }
}