import httpx
import src.config.logging_config as log
from typing import Optional

from src.config.constants import DEFAULT_URL, DEFAULT_TIMEOUT
# Supondo que o logging já foi configurado em outro lugar. 
# Remova este import se não houver necessidade de configurar aqui.

# Configuração do logging
log.logging.basicConfig()

class Downloader:
    def __init__(self):
        self.url = DEFAULT_URL
        self.timeout = DEFAULT_TIMEOUT

        if not self.url:
            raise ValueError("A URL não pode ser None.")
        
        if self.timeout is None:
            raise ValueError("O timeout não pode ser None.")
        
    def _download_zip_file(self) -> dict:

        log.logging.info(f"Iniciando download de: {self.url}")
        try:
            log.logging.warning("⚠️ Verificação SSL desativada para a URL: %s", self.url)

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
            log.logging.error(f"Erro HTTP: {e}")
            raise
        except Exception as e:
            log.logging.error(f"Erro inesperado no download: {e}")
            raise
