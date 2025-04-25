from pathlib import Path
import logging
from typing import Optional
from src.utils  import raise_io_error, raise_unexpected_error

class FileHandler:
    @staticmethod
    def _save_file_to_disk(file_info: dict, save_dir: str, logger: Optional[logging.Logger] = None) -> str:
        logger = logger or logging.getLogger("airflow.task")
        Path(save_dir).mkdir(parents=True, exist_ok=True)
        file_path = Path(save_dir) / file_info["filename"]
        try:
            with open(file_path, "wb") as f:
                f.write(file_info["content"])
            logger.info(f"Arquivo salvo em: {file_path} ({file_info['content_length']} bytes)")
            return str(file_path)
        except IOError as e:
            raise_io_error(e, logger)
        except Exception as e:
            raise_unexpected_error(e, logger)

        raise RuntimeError("Código inalcançável, erro deve ter sido lançado acima.")  # type: ignore[unreachable]
