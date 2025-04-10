import httpx
import logging
from typing import Optional
from typing import Dict, Any
from src.config.constants import DEFAULT_URL, DEFAULT_TIMEOUT
from ..utils.error_handlers import raise_http_error, raise_unexpected_error

class Downloader:
    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger or logging.getLogger("airflow.task")
        self.url = DEFAULT_URL
        self.timeout = DEFAULT_TIMEOUT

        if not self.url:
            self.logger.error(msg := "Valor inválido: a URL não pode ser None ou vazia.")
            raise ValueError(msg)
        
        if not self.timeout:
            self.logger.error(msg := "Valor inválido: o timeout não pode ser None.")
            raise ValueError(msg)

    def _download_zip_file(self) -> Dict[str, Any]:
        self.logger.info(f"Iniciando download de: {self.url}")
        try:
            self.logger.warning("⚠️ Verificação SSL desativada para a URL: %s", self.url)
            with httpx.stream("GET", self.url, timeout=self.timeout, verify=False) as response:
                response.raise_for_status()
                content = b''.join(response.iter_bytes())
                return {
                    "content": content,
                    "filename": self.url.split("/")[-1],
                    "content_type": response.headers.get("content-type", ""),
                    "content_length": len(content),
                    "status_code": response.status_code,
                }
        except httpx.HTTPError as e:
            raise_http_error(e, self.logger)
        except Exception as e:
            raise_unexpected_error(e, self.logger)
        raise RuntimeError("Código inalcançável, apenas para satisfazer o type checker.")  # type: ignore[unreachable]