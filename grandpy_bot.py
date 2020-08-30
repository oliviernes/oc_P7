from flaskapp import app

from logging.config import dictConfig
from flaskapp.backend.logging.logging_config import logging_config

dictConfig(logging_config)
