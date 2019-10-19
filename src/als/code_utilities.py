"""
Provides a set of utilities aimed at app developpers
"""
import logging
from functools import wraps
from time import time


def log(func):
    """
    Decorates a function to add logging.

    A log entry (DEBUG level) is printed with decorated function's qualified name and all its params.

    If the decorated function returns anything, a log entry (DEBUG level) is printed with decorated
    function's qualified name and return value(s).

    Logs are issued using is the logger named after the decorated function's enclosing module.

    :param func: The function to decorate
    :return: The decorated function
    """

    @wraps(func)
    def wrapped(*args, **kwargs):
        function_name = func.__qualname__
        logger = logging.getLogger(func.__module__)
        logger.debug(f"{function_name}() called with : {str(args)} - {str(kwargs)}")
        start_time = time()
        result = func(*args, **kwargs)
        end_time = time()
        logger.debug(f"{function_name}() returned {str(result)} in {(end_time - start_time) * 1000:0.3f} ms")
        return result
    return wrapped


# pylint: disable=W0201
class Timer:
    """
    A context manager, timing any portion of code it encloses.

    Basic usage :

    .. code-block:: python

        with Timer() as t:

            # your code here
            # it can be many lines
            pass

        _LOGGER.info(f"code ran in {t.elapsed_in_milli} ms.")

    The context manager exposes 2 attributes :

        - elapsed_in_milli (float) = elapsed time
        - elapsed_in_milli_as_str (str) = string representation of elapsed time with only 3 decimal positions

    """
    def __enter__(self):
        self.start = time()
        return self

    def __exit__(self, *args):
        self.end = time()
        self.elapsed_in_milli = (self.end - self.start) * 1000
        self.elapsed_in_milli_as_str = "%0.3f" % self.elapsed_in_milli


class AlsException(Exception):
    """
    Base class for all custom errors
    """
    def __init__(self, message, details):
        Exception.__init__(self)
        self.message = message
        self.details = details
