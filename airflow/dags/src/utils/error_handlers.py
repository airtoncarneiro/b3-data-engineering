import logging
from functools import wraps
from typing import Optional

def handle_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = kwargs.get("logger", logging.getLogger("airflow.task"))
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            raise
    return wrapper

def log_http_error(e, logger: Optional[logging.Logger] = None):
    logger = logger or logging.getLogger("airflow.task")
    logger.error(f"Erro HTTP: {e}")

def log_unexpected_error(e, logger: Optional[logging.Logger] = None):
    logger = logger or logging.getLogger("airflow.task")
    logger.error(f"Erro inesperado: {e}")

def log_io_error(e, logger: Optional[logging.Logger] = None):
    logger = logger or logging.getLogger("airflow.task")
    logger.error(f"Erro de I/O: {e}")

def log_bad_zip_error(e, logger: Optional[logging.Logger] = None):
    logger = logger or logging.getLogger("airflow.task")
    logger.error(f"Erro ao extrair arquivo ZIP inválido: {e}")

def raise_http_error(e, logger: Optional[logging.Logger] = None):
    logger = logger or logging.getLogger("airflow.task")
    log_http_error(e, logger)
    raise

def raise_unexpected_error(e, logger: Optional[logging.Logger] = None):
    logger = logger or logging.getLogger("airflow.task")
    log_unexpected_error(e, logger)
    raise

def raise_io_error(e, logger: Optional[logging.Logger] = None):
    logger = logger or logging.getLogger("airflow.task")
    log_io_error(e, logger)
    raise

def raise_bad_zip_error(e, logger: Optional[logging.Logger] = None):
    logger = logger or logging.getLogger("airflow.task")
    log_bad_zip_error(e, logger)
    raise