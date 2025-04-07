from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from datetime import timedelta
import logging
import src.config.logging_config as log
from typing import Dict, Any
from pathlib import Path
import os

from src.services.downloader import Downloader
from src.services.file_handler import FileHandler
from src.services.zip_extractor import ZipExtractor

# Define save_dir
save_dir = os.path.join(os.path.dirname(__file__), "downloads")
os.makedirs(save_dir, exist_ok=True)

# Configuração do logging
log.logging.basicConfig()

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

# 🚀 Wrappers com @task para o Airflow
@task
def _download_zip_file() -> Dict[str, Any]:
    downloader = Downloader()
    zip_data = downloader.download_zip_file()
    return zip_data

@task
def _save_file_to_disk(file_info: Dict[str, Any]) -> str:
    saved_path = FileHandler.save_file_to_disk(file_info, save_dir)
    return saved_path

@task
def _extract_zip_file(zip_path: str) -> Dict[str, Any]:
    zip_name = Path(zip_path).stem
    zip_dir = Path(zip_path).parent
    extract_dir = f"{zip_dir}/extracted_txt/{zip_name}"
    
    extractor = ZipExtractor(extract_dir)  # Agora é um diretório válido
    result = extractor.extract_zip_file(zip_path)
    return result

# 📅 DAG do Airflow
@dag(
    dag_id="b3_etl",
    default_args=default_args,
    schedule=None,
    start_date=days_ago(1),
    catchup=False,
    tags=["download", "zip", "httpx", "hibrido"],
    description="Pipeline híbrido testável como DAG ou script"
)
def final_download_and_extract_zip():
    # Define task dependencies
    downloaded = _download_zip_file()
    saved = _save_file_to_disk(downloaded) # type: ignore
    extracted = _extract_zip_file(saved) # type: ignore
    
    return extracted

if __name__ != "__main__":
    # 🎯 Execução direta no Airflow
    logging.info("Executando DAG pelo Airflow.")
    dag = final_download_and_extract_zip()
else:
    # 🎯 Execução direta no Python
    logging.info("Executando como script Python puro...")
    # Execute tasks directly when running as script
    downloaded = _download_zip_file.function()
    saved = _save_file_to_disk.function(downloaded)
    extracted = _extract_zip_file.function(saved)
    
    print(f"✅ Extração concluída: {extracted['total_files']} arquivos extraídos.")
    print(f"📦 Arquivo ZIP: {downloaded['filename']}")
    print(f"📂 Arquivos extraídos:")
    for arq in extracted['extracted_files']:
        print(f" - {arq}")
    print(f"📁 Diretório de extração: {extracted['extract_path']}")
