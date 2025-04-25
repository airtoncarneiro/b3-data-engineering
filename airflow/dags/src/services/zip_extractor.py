import zipfile
from typing import Dict, Any, Optional
from pathlib import Path
import logging
from src.utils  import raise_bad_zip_error, raise_unexpected_error

class ZipExtractor:
    def __init__(self, extract_path: str):
        self.extract_path = Path(extract_path)
        self.extract_path.mkdir(parents=True, exist_ok=True)

    def _extract_zip_file(self, zip_path: str, logger: Optional[logging.Logger] = None) -> Dict[str, Any]:
        logger = logger or logging.getLogger("airflow.task")
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                logger.info(f"Extracting {zip_path} to {self.extract_path}")
                zip_ref.extractall(self.extract_path)
                extracted_files = zip_ref.namelist()
                return {
                    "status": "success",
                    "total_files": len(extracted_files),
                    "extracted_files": extracted_files,
                    "extract_path": str(self.extract_path)
                }
        except zipfile.BadZipFile as e:
            raise_bad_zip_error(e, logger)
        except Exception as e:
            raise_unexpected_error(e, logger)

        raise RuntimeError("Código inalcançável, erro deve ter sido lançado acima.")  # type: ignore[unreachable]
