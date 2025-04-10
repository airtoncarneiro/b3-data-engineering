from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from datetime import timedelta
import logging
from typing import Dict, Any
from pathlib import Path
import os

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
}

@task
def log_start():
    logger = logging.getLogger("airflow.task")
    logger.info(f"INICIANDO DAG: b3_etl")
    return None

@task
def log_end(extracted: Dict[str, Any]) -> Dict[str, Any]:
    logger = logging.getLogger("airflow.task")
    logger.info(f"FINALIZOU DAG: b3_etl")
    return extracted

@task
def download_zip_file() -> str:
    from src.services.downloader import Downloader
    from src.services.file_handler import FileHandler
    logger = logging.getLogger("airflow.task")
    save_dir = os.path.join(os.path.dirname(__file__), "downloads")
    os.makedirs(save_dir, exist_ok=True)
    downloader = Downloader(logger=logger)
    zip_data = downloader._download_zip_file()
    saved_path = FileHandler._save_file_to_disk(zip_data, save_dir, logger=logger)
    logger.info(f"Arquivo ZIP baixado e salvo em: {saved_path}")
    return saved_path

@task
def extract_zip_file(zip_path: str) -> Dict[str, Any]:
    from src.services.zip_extractor import ZipExtractor
    logger = logging.getLogger("airflow.task")
    zip_name = Path(zip_path).stem
    zip_dir = Path(zip_path).parent
    extract_dir = f"{zip_dir}/extracted_txt/{zip_name}"
    extractor = ZipExtractor(extract_dir)
    result = extractor._extract_zip_file(zip_path, logger=logger)
    logger.info(f"Arquivo ZIP extraído em: {extract_dir}")
    logger.info(f"Arquivos extraídos: {result['extracted_files']}")
    return result

@dag(
    dag_id="b3_etl",
    default_args=default_args,
    schedule=None,
    start_date=days_ago(1),
    catchup=False,
    tags=["b3", "etl", "v 13"],
    description="Pipeline híbrido testável como DAG ou script Python (debugável)"
)
def final_download_and_extract_zip():
    start = log_start()
    downloaded = download_zip_file()
    extracted = extract_zip_file(downloaded)    # type: ignore
    end = log_end(extracted)    # type: ignore
    
    _ = start >> downloaded >> extracted >> end

    

dag = final_download_and_extract_zip()

if __name__ == "__main__" and os.environ.get("DEBUG_MODE", "false").lower() == "true":
    print("Executando em modo debug...")
    downloaded = download_zip_file.function()
    extracted = extract_zip_file.function(downloaded)
