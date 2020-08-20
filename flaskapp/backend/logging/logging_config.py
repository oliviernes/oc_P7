import logging

logging_config = dict(
    version=1,
    formatters={
        'f': {'format': '%(asctime)s %(name)s module name: %(module)s %(levelname)s function: %(funcName)s line number: %(lineno)d message: %(message)s' } 
    },
    handlers={
        'h': {'class': 'logging.handlers.RotatingFileHandler',
              'filename': 'flaskapp/backend/logging/logs.log',
              'maxBytes': 1024,
              'backupCount': 3,
              'level': 'DEBUG',
              'formatter': 'f',
              'encoding': 'utf8'}
    },

    root={
        'handlers': ['h'],
        'level': logging.DEBUG,
    },
)