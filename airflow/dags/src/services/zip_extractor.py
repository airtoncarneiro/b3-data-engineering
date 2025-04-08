import logging
import zipfile
from typing import Dict, Any
from pathlib import Path

class ZipExtractor:
    def __init__(self, extract_path: str):
        self.extract_path = Path(extract_path)
        self.extract_path.mkdir(parents=True, exist_ok=True)

    def _extract_zip_file(self, zip_path: str) -> Dict[str, Any]:
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                logging.info(f"Extracting {zip_path} to {self.extract_path}")
                zip_ref.extractall(self.extract_path)
                extracted_files = zip_ref.namelist()
                
                return {
                    "status": "success",
                    "total_files": len(extracted_files),
                    "extracted_files": extracted_files,
                    "extract_path": str(self.extract_path)
                }
        except zipfile.BadZipFile as e:
            logging.error(f"Error extracting ZIP file: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error during extraction: {e}")
            raise