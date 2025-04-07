import logging
from functools import wraps

def handle_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {str(e)}")
            raise
    return wrapper

def log_http_error(e):
    logging.error(f"Erro HTTP: {e}")

def log_unexpected_error(e):
    logging.error(f"Erro inesperado: {e}")

def raise_http_error(e):
    log_http_error(e)
    raise

def raise_unexpected_error(e):
    log_unexpected_error(e)
    raise