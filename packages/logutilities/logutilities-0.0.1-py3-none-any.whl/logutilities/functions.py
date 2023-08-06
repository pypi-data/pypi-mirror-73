import logging
import functools

logging.basicConfig(
    format='%(asctime)s %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=logging.INFO
)

def log_function(func):
    """Decorator for logging function name"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        logging.info("[{}]".format(func.__name__))
        res = func(*args, **kwargs)
        return res

    return wrapper