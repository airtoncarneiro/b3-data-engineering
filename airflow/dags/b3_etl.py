from airflow.decorators import dag, task
from airflow.models.baseoperator import chain
from airflow.operators.empty import EmptyOperator
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
def download_zip_file() -> str:
    from src.services.downloader import Downloader
    from src.services.file_handler import FileHandler
    from airflow.models import Variable
    logger = logging.getLogger("airflow.task")
    b3_download_all = Variable.get("B3_DOWNLOAD_ALL", default_var="false").lower() == "true"
    save_dir = os.path.join(os.path.dirname(__file__), "downloads")
    os.makedirs(save_dir, exist_ok=True)
    downloader = Downloader(logger=logger)
    zip_data = downloader._download_zip_file()
    saved_path = FileHandler._save_file_to_disk(zip_data, save_dir, logger=logger)
    logger.info(f"Arquivo ZIP baixado e salvo em: {saved_path}")
    Variable.set("B3_DOWNLOAD_ALL", "false")
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
    tags=["b3", "etl", "v 15"],
    description="Pipeline híbrido testável como DAG ou script Python (debugável)"
)
def final_download_and_extract_zip():
    downloaded = download_zip_file()
    extracted = extract_zip_file(downloaded)    # type: ignore
    inicio = EmptyOperator(task_id="inicio")
    fim = EmptyOperator(task_id="fim")    
    # _ = start >> downloaded >> extracted >> end
    chain(
        inicio,
        downloaded,
        extracted,
        fim
    )


dag = final_download_and_extract_zip()

if __name__ == "__main__" and os.environ.get("DEBUG_MODE", "false").lower() == "true":
    print("Executando em modo debug...")
    downloaded = download_zip_file.function()
    extracted = extract_zip_file.function(downloaded)
