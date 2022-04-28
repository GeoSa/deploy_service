import time
import logging
import logging.config


class UTCFormatter(logging.Formatter):
    """Formatter for UTC Dates
    """
    converter = time.gmtime


def init_logger(level: str) -> None:
    """Configure Logging
    """
    logging.config.dictConfig({
        'disable_existing_loggers': False,
        'version': 1,
        'formatters': {
            'short': {
                '()': UTCFormatter,
                'format': '%(levelname)s %(message)s'
            },
            'verbose': {
                '()': UTCFormatter,
                'format': '%(asctime)s %(levelname)s %(name)s %(filename)s:%(lineno)s %(message)s'
            },
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'formatter': 'short',
                'class': 'logging.StreamHandler',
            },
            'file': {
                'level': 'INFO',
                'formatter': 'verbose',
                'filename': 'logs/logs.log',
                'utc': True,
                'when': 'midnight',
                'encoding': 'utf-8',
                'backupCount': 6,
                'class': 'logging.handlers.TimedRotatingFileHandler',
            }
        },
        'loggers': {
            'bot': {
                'handlers': ['console', 'file'],
                'level': level,
            }
        },
    })
