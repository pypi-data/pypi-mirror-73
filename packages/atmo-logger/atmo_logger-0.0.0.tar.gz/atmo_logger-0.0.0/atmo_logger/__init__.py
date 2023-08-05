"""
Logging for CyVerse Atmosphere.
* Provides two separate log levels.
* One log level for dependencies and one for the application.
"""

from __future__ import absolute_import
import logging
import sys
from . import version

__title__ = 'atmo_logger'
__version__ = version.get_version(form='short')
__author__ = 'CyVerse'
__license__ = 'University of Arizona'
__copyright__ = 'Copyright 2020 University of Arizona'


logger = None

VERSION = version.VERSION
version = version.get_version(form='verbose')

LOGGER_NAME = "atmo_logger"
LOG_FILENAME = "./atmo_logger.log"
APP_LOGGING_LEVEL = logging.DEBUG
DEP_LOGGING_LEVEL = logging.INFO

def initialize(logger_name=LOGGER_NAME,
               log_filename=LOG_FILENAME,
               app_logging_level=APP_LOGGING_LEVEL,
               dep_logging_level=DEP_LOGGING_LEVEL,
               format=None,
               logger_class=None,
               handlers=[],
               global_logger=True):
    """
    Constructs and initializes a `logging.Logger` object.
    Returns :class:`logging.Logger` object.
    :param logger_name: name of the new logger.
    :param log_filename: The log file location :class:`str` or None.
    :param app_logging_level: The logging level to use for the application.
    :param dep_logging_level: The logging level to use for dependencies.
    :param format: The format string to use :class: `str` or None.
    :param logger_class: The logger class to use
    :param handlers: List of handler instances to add.
    :param global_logger: If true set atmo_logger's global logger variable to this logger.
    """
    # If there is no format, use a default format.
    if not format:
        format = "%(asctime)s %(name)s-%(levelname)s "\
                 + "[%(pathname)s %(lineno)d] %(message)s"
    formatter = logging.Formatter(format)

    # Setup the root logging for dependencies, etc.
    if log_filename:
        logging.basicConfig(
            level=dep_logging_level,
            format=format,
            filename=log_filename,
            filemode='a+')
    else:
        logging.basicConfig(
            level=dep_logging_level,
            format=format)

    # Setup and add separate application logging.
    if logger_class:
        original_class = logging.getLoggerClass()
        logging.setLoggerClass(logger_class)
        new_logger = logging.getLogger(logger_name)
        logging.setLoggerClass(original_class)
    else:
        new_logger = logging.getLogger(logger_name)

    # Set the app logging level.
    new_logger.setLevel(app_logging_level)  # required to get level to apply.

    # Set the global_logger by default.
    if global_logger:
        global logger
        logger = new_logger

    for handler in handlers:
        handler.setFormatter(formatter)
        handler.setLevel(app_logging_level)
        new_logger.addHandler(handler)
    return new_logger
