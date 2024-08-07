# pylint: disable=C0413,C0411
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-hid0esb0%k#8u@o_o4m%g)s_0hynyoev&x^t(l80oq+w9+%77k"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


try:
    from .local import *
except ImportError:
    pass


__base_path__ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
__log_path__ = os.path.join(__base_path__, "log")

if not os.path.exists(__log_path__):
    os.makedirs(__log_path__)
from datetime import datetime

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{levelname}][{asctime}][{module}][{process:d}][{thread:d}][{message}]",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            'formatter': 'verbose',
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": os.path.join(__log_path__, 
                                        f"django_logfile_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')[:23]}.log"),
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": True,
        },
    },
}
