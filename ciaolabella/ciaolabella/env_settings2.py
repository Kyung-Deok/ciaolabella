from datetime import date

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
        'test': {
            'format': '%(user_id)s %(user_gender)s %(user_age)s %(radius_km)s %(searchclick_location)s %(searchclick_time)s',
        },
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
        'test': {
            'level': 'INFO',
            'encoding': 'utf-8',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': f'/home/multi/ciaolabella2/ciaolabella/logs/test/test.log',
            # 'maxBytes': 1024*1024*5,  # 5 MB
            'formatter': 'test',
            'backupCount': 5,
        },
        'file': {
            'level': 'INFO',
            'encoding': 'utf-8',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': f'/home/multi/ciaolabella2/ciaolabella/logs/user/{date.today().isoformat()}.log',
            # 'maxBytes': 1024*1024*5,  # 5 MB
            'formatter': 'standard',
            'backupCount': 5,
        },
        'errors': {
            'encoding': 'utf-8',
            'level': 'ERROR',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': f'/home/multi/ciaolabella2/ciaolabella/logs/error/{date.today().isoformat()}.log',
            # 'maxBytes': 1024*1024*5,  # 5 MB
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
        '': {
            'level': 'INFO',
            'handlers': ['file', 'errors', 'mail_admins'],
        },
        'django': {
            'handlers': ['console'],
        },
        'userlog.duration': {
            'handlers': ['file'],
            'level': 'INFO',
        },
        'userlog.menuclick': {
            'handlers': ['file'],
            'level': 'INFO',
        },
        'userlog.ecopoint': {
            'handlers': ['file'],
            'level': 'INFO',
        },
        'userlog.nolabel': {
            'handlers': ['file'],
            'level': 'INFO',
        },
        'userlog.lesswaste': {
            'handlers': ['test'],
            'level': 'INFO',
        },
    }
}